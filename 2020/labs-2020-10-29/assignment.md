
# Tasks

## clean tracks w.r.t. `who` and `w`

Not giving precise task description on purpose. Do the research first.

This is standard [hacker tool](https://www.imdb.com/title/tt0113957/?ref_=nv_sr_1?ref_=nv_sr_1) from the 90's,
i.e. write a program that removes entries matching specification from the
database used by these programs.

Avoid searching for ready made solutions (obviously, that would spoil the fun).

Do not use high level APIs (those available in libc) that access/modify the database. It should be possible
to implement the core functionality using only syscalls (today's lecture and the last 2 lectures on file API).

Make the program flexible in terms of specifying what to clean (getopt).

Be as thorough in covering the tracks as possible (metadata!).

Write test cases.
