# RunUp

![GitHub](https://img.shields.io/github/license/kennylajara/RunUp?style=for-the-badge&color=%230374b4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RunUp?label=Python%20Support&style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/RunUp?style=for-the-badge&color=%230374b4&label=Version&logoColor=%23ffffff)


RunUp is a backup system that can be managed by command line. It is intended to be easy to use, secure and fast.

### Why yet another backup solution?

Most backup solutions are good at making full backups, but this can be time-consuming and unchanged data is replicated each time a new backup is made.

Some other solutions implement differential backups and incremental backups, two strategies that _partially_ solve this drawback. But that's the problem with them.... "partially". With those strategies you can create the backups faster but now restoring the data takes a longer time, so, how do you solve it? By creating full backups from time to time and partial backups thereafter (either incremental or differential).

These strategies reduce data duplication and partial backups are created faster (the full backups that you need to create every now an then still take the same), but this is not for free, data restoration would be slower than if you just makes full bakups. Honestly, these are not so bad strategies, but I think we can do better.

The other options are the Git based solutions. Well, Git is excellent for code versioning but when you talk about backups... let's says that this is not what it was designed for.

Git history can't be modified, to do simple tasks like deleting older restore points or moving some files to cold storage, you'd have to resort to some dubious data manipulation. I admit, I don't know how they implement it (or if they even do), but I'm not sure I want to know.... And let's not forget the well-known problem of large files. Let's quote what the creator of Git said about it:

> And yes, then there’s the “big file” issues. I really don’t know what to do about huge files. We suck at them, I know.
> 
> — Linus Torvalds ([source](https://towardsdatascience.com/data-versioning-all-you-need-to-know-7077aa5ed6d1#d5e7))

So why another backup solution? Because we have to finally solve these problems and that's what this tool does by creating "fragmented backups", a new backup strategy that not only reduces both backup creation and restore time, but avoids data duplication altogether.

## Usage

Unfortunately it is not ready yet, so it cannot be used. I am working hard on it.

## Contribution

Contributions are welcome, either as an idea or as an implementations in the form of Pull Request. Do not hesitate to open a new issue to clarify doubts that may help the development of the product.

## License

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at [https://mozilla.org/MPL/2.0/](https://mozilla.org/MPL/2.0/).
