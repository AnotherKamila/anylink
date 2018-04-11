anylink
=======

Easily link to any file stored on your server: create a shareable (but unguessable) link to anything.

Just like cloud services' "Share -> Anyone with the link", but without the hassle of uploading stuff -- if it's already on your server, then it should be easier! Links can also expire automatically, so you don't have to give people access forever. All access is read-only.

Comes with a nice commandline interface -- just type `./url myserver path/to/file`.

Entire directories can be shared too -- just add a directory by typing `./url myserver path/to/dir`.

Trivial to set up -- needs just Python.

Usage Tips
----------

The commandline interface (`./url`) is pretty awesome, but if you want even more awesomeness, you can add a shell alias, or even integrate it with graphical file managers via a plugin script / custom actions (assuming your file manager knows something about the files on the server).

This is especially nice if you use another tool to synchronize files between your local machine and your server: for example, I use [Syncthing](https://syncthing.net/) to mirror my home directory between my laptop and server, so the local paths are the same as the remote paths. That way I can execute the command on my laptop against the local files, and it does the right thing because the paths are the same.

 The `url` script is secretly just a wrapper around SSH, so you can use SSH server aliases or things which aren't FQDNs, such as `localhost`.

Security
--------

The URLs are of the form `/uuid/filename`. Anything other than a readable file with the correct UUID and filename returns a 404 (to avoid leaking any info). The key is a 128-bit random-based UUID, therefore the URLs are unguessable. By default URLs expire after 30 days.

Note that the filenames (but not the full paths) are revealed.

Only GET (and HEAD) requests are supported and the program never writes any file. If you want to, you can run it as a user that has only read access.

Links cannot be created remotely -- the `url` script actually just `ssh`es to `myserver` and appends a line to the `links.csv` file. Therefore a remote attacker without access to the server can't do anything.
