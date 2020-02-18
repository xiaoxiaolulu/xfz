# gulo

This project serves as an example security flaw that `npx` typos can lead to.

## I ran gulo. Has my data been compromised?

Well, it might have been compromised, but `gulo` had nothing to do with it; check `gulo`'s source code. It just logs a warning.

## How can I prevent arbitrary code execution?

- Do not use `npx` directly. Look up `--shell-auto-fallback`.
- Learn to type

## I don't care. What's the "worst" that could be executed?

Anything that your machine user can run. And even more using privilege escalation. Consider your passwords leaked, bank accounts emptied and identity stolen.