"""Private, local file handling shared by the v9 per-user stores.

Project owner: Antonio T. Smith Jr. / Density6 LLC

Every v9 store that holds a writer's own material (the firsthand vault, the
review ledger) goes through these helpers, so the rules live in one place:

- POSIX only. Secure relative opening needs O_NOFOLLOW, O_DIRECTORY and
  dir_fd; where they are absent (Windows) every call refuses with
  PLATFORM_UNSUPPORTED rather than falling back to an unsafe path walk.
- A private folder is created 0700 and refused if it is a symlink.
- A private folder may not sit inside a git working tree, so a writer's
  notes cannot be committed, pushed or picked up by CI by accident.
- Files are created 0600 with O_NOFOLLOW; a record that must never be
  overwritten is created with O_EXCL.
"""
import errno
import json
import os
import stat
from pathlib import Path


class StoreRefusal(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code


def require_posix():
    if (not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY")
            or os.open not in os.supports_dir_fd):
        raise StoreRefusal("PLATFORM_UNSUPPORTED",
                           "secure relative file opening (O_NOFOLLOW, dir_fd) is unavailable on this "
                           "platform; private v9 stores refuse to run rather than risk following a link")


def inside_git_worktree(path):
    """True if `path` or any parent holds a .git entry."""
    probe = Path(path).resolve()
    for folder in [probe] + list(probe.parents):
        if os.path.lexists(str(folder / ".git")):
            return True
    return False


def open_private_root(path, create=False):
    """Open (and optionally create) a private folder; returns a directory fd."""
    require_posix()
    if not isinstance(path, str) or not path or "\x00" in path:
        raise StoreRefusal("PATH_INVALID", "a private folder path is required")
    target = Path(path).expanduser()
    if os.path.islink(str(target)):
        raise StoreRefusal("PATH_SYMLINK", "the private folder is a symlink")
    if not target.exists():
        if not create:
            raise StoreRefusal("STORE_MISSING", "no private store at %s" % target)
        if inside_git_worktree(target.parent if target.parent.exists() else Path.cwd()):
            raise StoreRefusal("STORE_INSIDE_REPOSITORY",
                               "private material may not live inside a git working tree; choose a folder "
                               "outside any repository")
        os.makedirs(str(target), mode=0o700)
    if inside_git_worktree(target):
        raise StoreRefusal("STORE_INSIDE_REPOSITORY",
                           "private material may not live inside a git working tree; choose a folder outside "
                           "any repository")
    fd = os.open(str(target.resolve()), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    info = os.fstat(fd)
    if info.st_mode & 0o077:
        os.fchmod(fd, 0o700)
    return fd


def open_subdir(dirfd, name, create=False):
    try:
        return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=dirfd)
    except FileNotFoundError:
        if not create:
            raise
        os.mkdir(name, 0o700, dir_fd=dirfd)
        return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=dirfd)


def read_file(dirfd, name, limit):
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dirfd)
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise StoreRefusal("PATH_SYMLINK", "%s is a symlink" % name)
        raise
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise StoreRefusal("PATH_NOT_FILE", "%s is not a regular file" % name)
        if info.st_size > limit:
            raise StoreRefusal("FILE_TOO_LARGE", "%s exceeds %d bytes" % (name, limit))
        with os.fdopen(fd, "rb", closefd=False) as inp:
            data = inp.read(limit + 1)
    finally:
        os.close(fd)
    if len(data) > limit:
        raise StoreRefusal("FILE_TOO_LARGE", "%s grew past %d bytes" % (name, limit))
    return data


def write_new(dirfd, name, data):
    """Create a file that must not already exist (0600, never a link)."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    fd = os.open(name, flags, 0o600, dir_fd=dirfd)
    with os.fdopen(fd, "wb") as out:
        out.write(data)


def replace_file(dirfd, name, data):
    """Write `name` atomically: a fresh temp file, then rename over it."""
    temp = ".%s.tmp-%d" % (name, os.getpid())
    try:
        os.unlink(temp, dir_fd=dirfd)
    except FileNotFoundError:
        pass
    write_new(dirfd, temp, data)
    os.replace(temp, name, src_dir_fd=dirfd, dst_dir_fd=dirfd)


def append_line(dirfd, name, line):
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW
    fd = os.open(name, flags, 0o600, dir_fd=dirfd)
    with os.fdopen(fd, "a", encoding="utf-8") as out:
        out.write(line.rstrip("\n") + "\n")


def remove_file(dirfd, name):
    try:
        os.unlink(name, dir_fd=dirfd)
    except FileNotFoundError:
        pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
