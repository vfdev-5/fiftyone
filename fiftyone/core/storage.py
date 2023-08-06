"""
File storage utilities.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from datetime import datetime
import json
import logging
import multiprocessing.dummy
import os
import re
import six
import shutil
import tempfile

import jsonlines
import yaml

import eta.core.serial as etas
import eta.core.utils as etau

import fiftyone as fo
import fiftyone.core.utils as fou


logger = logging.getLogger(__name__)


def normalize_path(path):
    """Normalizes the given path.

    Paths are sanitized via::

        os.path.abspath(os.path.expanduser(path))

    Args:
        path: a path

    Returns:
        the normalized path
    """
    return os.path.abspath(os.path.expanduser(path))


def make_temp_dir(basedir=None):
    """Makes a temporary directory.

    Args:
        basedir (None): an optional directory in which to create the new
            directory. The default is
            ``fiftyone.config.default_dataset_dir``

    Returns:
        the temporary directory path
    """
    if basedir is None:
        basedir = fo.config.default_dataset_dir

    ensure_dir(basedir)
    return tempfile.mkdtemp(dir=basedir)


class TempDir(object):
    """Context manager that creates and destroys a temporary directory.

    Args:
        basedir (None): an optional directory in which to create the new
            directory. The default is ``fiftyone.config.default_dataset_dir``
    """

    def __init__(self, basedir=None):
        self._basedir = basedir
        self._name = None

    def __enter__(self):
        self._name = make_temp_dir(basedir=self._basedir)
        return self._name

    def __exit__(self, *args):
        delete_dir(self._name)


def make_archive(dirpath, archive_path, cleanup=False):
    """Makes an archive containing the given directory.

    Supported formats include ``.zip``, ``.tar``, ``.tar.gz``, ``.tgz``,
    ``.tar.bz`` and ``.tbz``.

    Args:
        dirpath: the directory to archive
        archive_path: the archive path to write
        cleanup (False): whether to delete the directory after archiving it
    """
    logger.info("Making archive...")
    etau.make_archive(dirpath, archive_path)

    if cleanup:
        delete_dir(dirpath)


def extract_archive(archive_path, outdir=None, cleanup=False):
    """Extracts the contents of an archive.

    The following formats are guaranteed to work:
    ``.zip``, ``.tar``, ``.tar.gz``, ``.tgz``, ``.tar.bz``, ``.tbz``.

    If an archive *not* in the above list is found, extraction will be
    attempted via the ``patool`` package, which supports many formats but may
    require that additional system packages be installed.

    Args:
        archive_path: the archive path
        outdir (None): the directory into which to extract the archive. By
            default, the directory containing the archive is used
        cleanup (False): whether to delete the archive after extraction
    """
    if outdir is None:
        outdir = os.path.dirname(archive_path) or "."

    logger.info("Extracting archive...")
    etau.extract_archive(archive_path, outdir=outdir)

    if cleanup:
        delete_file(archive_path)


def ensure_empty_dir(dirpath, cleanup=False):
    """Ensures that the given directory exists and is empty.

    Args:
        dirpath: the directory path
        cleanup (False): whether to delete any existing directory contents

    Raises:
        ValueError: if the directory is not empty and ``cleanup`` is False
    """
    etau.ensure_empty_dir(dirpath, cleanup=cleanup)


def ensure_basedir(path):
    """Makes the base directory of the given path, if necessary.

    Args:
        path: the filepath
    """
    etau.ensure_basedir(path)


def ensure_dir(dirpath):
    """Makes the given directory, if necessary.

    Args:
        dirpath: the directory path
    """
    etau.ensure_dir(dirpath)


def read_file(path, binary=False):
    """Reads the file.

    Args:
        path: the filepath
        binary (False): whether to read the file in binary mode

    Returns:
        the file contents
    """
    mode = "rb" if binary else "r"
    with open(path, mode) as f:
        return f.read()


def write_file(str_or_bytes, path):
    """Writes the given string/bytes to a file.

    If a string is provided, it is encoded via ``.encode()``.

    Args:
        str_or_bytes: the string or bytes
        path: the filepath
    """
    ensure_basedir(path)
    with open(path, "wb") as f:
        f.write(_to_bytes(str_or_bytes))


def load_json(path_or_str):
    """Loads JSON from the input argument.

    Args:
        path_or_str: the filepath or JSON string

    Returns:
        the loaded JSON
    """
    try:
        return json.loads(path_or_str)
    except ValueError:
        pass

    if os.path.isfile(path_or_str):
        return read_json(path_or_str)

    raise ValueError("Unable to load JSON from '%s'" % path_or_str)


def read_json(path):
    """Reads a JSON file.

    Args:
        path: the filepath

    Returns:
        the JSON data
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except ValueError:
        raise ValueError("Unable to parse JSON file '%s'" % path)


def write_json(d, path, pretty_print=False):
    """Writes JSON object to file.

    Args:
        d: JSON data
        path: the filepath
        pretty_print (False): whether to render the JSON in human readable
            format with newlines and indentations
    """
    s = etas.json_to_str(d, pretty_print=pretty_print)
    write_file(s, path)


def load_ndjson(path_or_str):
    """Loads NDJSON from the input argument.

    Args:
        path_or_str: the filepath or NDJSON string

    Returns:
        a list of JSON dicts
    """
    try:
        return etas.load_ndjson(path_or_str)
    except ValueError:
        pass

    if os.path.isfile(path_or_str):
        return read_ndjson(path_or_str)

    raise ValueError("Unable to load NDJSON from '%s'" % path_or_str)


def read_ndjson(path):
    """Reads an NDJSON file.

    Args:
        path: the filepath

    Returns:
        a list of JSON dicts
    """
    with open(path, "r") as f:
        with jsonlines.Reader(f) as r:
            return list(r.iter(skip_empty=True))


def write_ndjson(obj, path):
    """Writes the list of JSON dicts in NDJSON format.

    Args:
        obj: a list of JSON dicts
        path: the filepath
    """
    with open(path, "w") as f:
        with jsonlines.Writer(f) as w:
            w.write_all(obj)


def read_yaml(path):
    """Reads a YAML file.

    Args:
        path: the filepath

    Returns:
        a list of JSON dicts
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)


def write_yaml(obj, path, **kwargs):
    """Writes the object to a YAML file.

    Args:
        obj: a Python object
        path: the filepath
        **kwargs: optional arguments for ``yaml.dump(..., **kwargs)``
    """
    with open(path, "w") as f:
        return yaml.dump(obj, stream=f, **kwargs)


def list_files(
    dirpath,
    abs_paths=False,
    recursive=False,
    include_hidden_files=False,
    return_metadata=False,
    sort=True,
):
    """Lists the files in the given directory.

    If the directory does not exist, an empty list is returned.

    Args:
        dirpath: the path to the directory to list
        abs_paths (False): whether to return the absolute paths to the files
        recursive (False): whether to recursively traverse subdirectories
        include_hidden_files (False): whether to include dot files
        return_metadata (False): whether to return metadata dicts for each file
            instead of filepaths
        sort (True): whether to sort the list of files

    Returns:
        a list of filepaths or metadata dicts
    """
    if not os.path.isdir(dirpath):
        return []

    filepaths = etau.list_files(
        dirpath,
        abs_paths=abs_paths,
        recursive=recursive,
        include_hidden_files=include_hidden_files,
        sort=sort,
    )

    if not return_metadata:
        return filepaths

    metadata = []
    for filepath in filepaths:
        if abs_paths:
            fp = filepath
        else:
            fp = os.path.join(dirpath, filepath)

        m = _get_local_metadata(fp)
        m["filepath"] = filepath
        metadata.append(m)

    return metadata


def _get_local_metadata(filepath):
    s = os.stat(filepath)
    return {
        "name": os.path.basename(filepath),
        "size": s.st_size,
        "last_modified": datetime.fromtimestamp(s.st_mtime),
    }


def list_subdirs(dirpath, abs_paths=False, recursive=False):
    """Lists the subdirectories in the given directory, sorted alphabetically
    and excluding hidden directories.

    Args:
        dirpath: the path to the directory to list
        abs_paths (False): whether to return absolute paths
        recursive (False): whether to recursively traverse subdirectories

    Returns:
        a list of subdirectories
    """
    return etau.list_subdirs(dirpath, abs_paths=abs_paths, recursive=recursive)


def list_buckets(_, abs_paths=False):
    """Lists the available buckets in the given file system.

    This method returns subdirectories of ``/`` (or the current drive on
    Windows).

    Args:
        _: an unused value
        abs_paths (False): whether to return absolute paths

    Returns:
        a list of buckets
    """
    root = os.path.abspath(os.sep)
    return etau.list_subdirs(root, abs_paths=abs_paths, recursive=False)


def get_glob_matches(glob_patt):
    """Returns a list of file paths matching the given glob pattern.

    The matches are returned in sorted order.

    Args:
        glob_patt: a glob pattern like ``/path/to/files-*.jpg`` or
            ``s3://path/to/files-*-*.jpg``

    Returns:
        a list of file paths
    """
    return etau.get_glob_matches(glob_patt)


def get_glob_root(glob_patt):
    """Finds the root directory of the given glob pattern, i.e., the deepest
    subdirectory that contains no glob characters.

    Args:
        glob_patt: a glob pattern like ``/path/to/files-*.jpg`` or
            ``s3://path/to/files-*-*.jpg``

    Returns:
        a tuple of:

        -   the root
        -   True/False whether the pattern contains any special characters
    """
    special_chars = "*?[]"

    # Remove escapes around special characters
    replacers = [("[%s]" % s, s) for s in special_chars]
    glob_patt = etau.replace_strings(glob_patt, replacers)

    # @todo optimization: don't split on specials that were previously escaped,
    # as this could cause much more recursive listing than necessary
    split_patt = "|".join(map(re.escape, special_chars))
    root = re.split(split_patt, glob_patt, 1)[0]

    found_special = root != glob_patt
    root = os.path.dirname(root)

    return root, found_special


def copy_file(inpath, outpath):
    """Copies the input file to the output location.

    Args:
        inpath: the input path
        outpath: the output path
    """
    _copy_file(inpath, outpath, cleanup=False)


def copy_files(inpaths, outpaths, skip_failures=False, progress=False):
    """Copies the files to the given locations.

    Args:
        inpaths: a list of input paths
        outpaths: a list of output paths
        skip_failures (False): whether to gracefully continue without raising
            an error if an operation fails
        progress (False): whether to render a progress bar tracking the status
            of the operation
    """
    _copy_files(inpaths, outpaths, skip_failures, progress)


def copy_dir(
    indir, outdir, overwrite=True, skip_failures=False, progress=False
):
    """Copies the input directory to the output directory.

    Args:
        indir: the input directory
        outdir: the output directory
        overwrite (True): whether to delete an existing output directory (True)
            or merge its contents (False)
        skip_failures (False): whether to gracefully continue without raising
            an error if an operation fails
        progress (False): whether to render a progress bar tracking the status
            of the operation
    """
    if overwrite and os.path.isdir(outdir):
        delete_dir(outdir)

    files = list_files(
        indir, include_hidden_files=True, recursive=True, sort=False
    )
    inpaths = [os.path.join(indir, f) for f in files]
    outpaths = [os.path.join(outdir, f) for f in files]
    copy_files(
        inpaths, outpaths, skip_failures=skip_failures, progress=progress
    )


def move_file(inpath, outpath):
    """Moves the given file to a new location.

    Args:
        inpath: the input path
        outpath: the output path
    """
    _copy_file(inpath, outpath, cleanup=True)


def move_files(inpaths, outpaths, skip_failures=False, progress=False):
    """Moves the files to the given locations.

    Args:
        inpaths: a list of input paths
        outpaths: a list of output paths
        skip_failures (False): whether to gracefully continue without raising
            an error if an operation fails
        progress (False): whether to render a progress bar tracking the status
            of the operation
    """
    tasks = [(i, o, skip_failures) for i, o in zip(inpaths, outpaths)]
    if tasks:
        _run(_do_move_file, tasks, progress=progress)


def move_dir(
    indir, outdir, overwrite=True, skip_failures=False, progress=False
):
    """Moves the contents of the given directory into the given output
    directory.

    Args:
        indir: the input directory
        outdir: the output directory
        overwrite (True): whether to delete an existing output directory (True)
            or merge its contents (False)
        skip_failures (False): whether to gracefully continue without raising
            an error if an operation fails
        progress (False): whether to render a progress bar tracking the status
            of the operation
    """
    if overwrite and os.path.isdir(outdir):
        delete_dir(outdir)

    if overwrite:
        etau.ensure_basedir(outdir)
        shutil.move(indir, outdir)


def delete_file(path):
    """Deletes the file at the given path.

    Any empty directories are also recursively deleted from the resulting
    directory tree.

    Args:
        path: the filepath
    """
    _delete_file(path)


def delete_files(paths, skip_failures=False, progress=False):
    """Deletes the files from the given locations.

    Any empty directories are also recursively deleted from the resulting
    directory tree.

    Args:
        paths: a list of paths
        skip_failures (False): whether to gracefully continue without raising
            an error if an operation fails
        progress (False): whether to render a progress bar tracking the status
            of the operation
    """
    tasks = [(p, skip_failures) for p in paths]
    if tasks:
        _run(_do_delete_file, tasks, progress=progress)


def delete_dir(dirpath):
    """Deletes the given directory and recursively deletes any empty
    directories from the resulting directory tree.

    Args:
        dirpath: the directory path
    """
    etau.delete_dir(dirpath)


def run(fcn, tasks, num_workers=None, progress=False):
    """Applies the given function to each element of the given tasks.

    Args:
        fcn: a function that accepts a single argument
        tasks: an iterable of function aguments
        num_workers (None): the number of threads to use. By default,
            ``multiprocessing.cpu_count()`` is used
        progress (False): whether to render a progress bar tracking the status
            of the operation

    Returns:
        the list of function outputs
    """
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    try:
        num_tasks = len(tasks)
    except:
        num_tasks = None

    kwargs = dict(total=num_tasks, iters_str="files", quiet=not progress)

    if not num_workers or num_workers <= 1:
        with fou.ProgressBar(**kwargs) as pb:
            results = [fcn(task) for task in pb(tasks)]
    else:
        with multiprocessing.dummy.Pool(processes=num_workers) as pool:
            with fou.ProgressBar(**kwargs) as pb:
                results = list(pb(pool.imap(fcn, tasks)))

    return results


def _copy_files(inpaths, outpaths, skip_failures, progress):
    tasks = [(i, o, skip_failures) for i, o in zip(inpaths, outpaths)]
    if tasks:
        _run(_do_copy_file, tasks, progress=progress)


def _run(fcn, tasks, num_workers=None, progress=False):
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    try:
        num_tasks = len(tasks)
    except:
        num_tasks = None

    kwargs = dict(total=num_tasks, iters_str="files", quiet=not progress)

    if not num_workers or num_workers <= 1:
        with fou.ProgressBar(**kwargs) as pb:
            for task in pb(tasks):
                fcn(task)
    else:
        with multiprocessing.dummy.Pool(processes=num_workers) as pool:
            with fou.ProgressBar(**kwargs) as pb:
                for _ in pb(pool.imap_unordered(fcn, tasks)):
                    pass


def _do_copy_file(arg):
    inpath, outpath, skip_failures = arg

    try:
        _copy_file(inpath, outpath, cleanup=False)
    except Exception as e:
        if not skip_failures:
            raise

        if skip_failures != "ignore":
            logger.warning(e)


def _do_move_file(arg):
    inpath, outpath, skip_failures = arg

    try:
        _copy_file(inpath, outpath, cleanup=True)
    except Exception as e:
        if not skip_failures:
            raise

        if skip_failures != "ignore":
            logger.warning(e)


def _do_delete_file(arg):
    filepath, skip_failures = arg

    try:
        _delete_file(filepath)
    except Exception as e:
        if not skip_failures:
            raise

        if skip_failures != "ignore":
            logger.warning(e)


def _copy_file(inpath, outpath, cleanup=False):
    etau.ensure_basedir(outpath)
    if cleanup:
        shutil.move(inpath, outpath)


def _delete_file(filepath):
    etau.delete_file(filepath)


def _to_bytes(val, encoding="utf-8"):
    b = val.encode(encoding) if isinstance(val, six.text_type) else val
    if not isinstance(b, six.binary_type):
        raise TypeError("Failed to convert %s to bytes" % type(b))

    return b
