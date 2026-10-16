\# Lab 5: Static Code Analysis — Issues Found



| # | Issue | Type | Tool | Severity | Line(s) | Description | Fix Approach |

|---|-------|------|------|----------|---------|-------------|--------------|

| 1 | Trojan source (B613) | Security | Bandit | High | 22 | Hidden Unicode bidi characters make the "comment" part of the string, so `isOfficer` returns True for every role | Rewrote as `return role == "officer"` |

| 2 | Weak MD5 hash (B324) | Security | Bandit | High | 17 | MD5 is cryptographically broken | Replaced with `hashlib.sha256` |

| 3 | Unsafe XML parsing (B319/B409) | Security | Bandit | Medium | 7, 75 | `xml.dom.pulldom` is vulnerable to XML attacks (e.g. entity expansion) | Used `defusedxml.pulldom.parseString` |

| 4 | Hardcoded password (B105) | Security | Bandit | Low | 9 | Admin password stored in source code | Read from `ADMIN\_PASSWORD` environment variable |

| 5 | Insecure random (B311) | Security | Bandit | Low | 72 | `random` is predictable, unsuitable for receipt numbers | Used `secrets.randbelow` |

| 6 | try/except/pass (B110), bare except (E722) | Bug | Bandit, Flake8 | Low | 79–83 | Silently swallows every error | Removed the unnecessary try/except |

| 7 | Unused imports (F401) | Style | Flake8 | Low | 2–4 | `sys`, `json`, `random` imported but unused | Removed them |

| 8 | Unused variables (F841) | Style | Flake8 | Low | 32, 45, 55 | `receipt`, `total`, `now` assigned but never used | Removed / receipt now returned |

| 9 | Formatting (E302, E501, W291) | Style | Flake8 | Low | Many | Missing blank lines, long lines, trailing whitespace | Reformatted to PEP 8 |

| 10 | Late-binding lambda (cell-var-from-loop) | Bug | Pylint | Medium | 68 | Every lambda captures the last `name`, so all announcements show NOTA | Replaced with a list comprehension over `candidates` |

| 11 | Naming, docstrings, redefined-outer-name | Quality | Pylint | Low | Whole file | camelCase names, no docstrings, `ballots` parameter shadows global | snake\_case, added docstrings, renamed to `ballot\_list` |

| 12 | Off-by-one voting age | Logic bug | Manual | High | 16 | `age > 18` rejects 18-year-olds | Changed to `age >= VOTING\_AGE` |

| 13 | Double voting allowed | Logic bug | Manual | High | 26–34 | `voted` flag never checked | Reject voters who already voted |

| 14 | No candidate validation | Logic bug | Manual | Medium | 31, 80 | `'bob'` counted as a separate candidate | Reject candidates not in `candidates` |

| 15 | Polls close check off by one | Logic bug | Manual | Medium | 29 | `hour > 18` accepts an 18:30 vote | Changed to `hour >= POLLS\_CLOSE\_HOUR` |

| 16 | Wrong turnout / divide by zero | Logic bug | Manual | Medium | 52, 56 | Turnout counted ballots (166%); `//` truncates; crashes with no ballots/voters | Count voters who voted; use `/`; guard zero |

| 17 | Postal ballots unchecked | Logic bug | Manual | Medium | 74–84 | Imports ballots without checking voter registration or prior vote | Validate voter and candidate before counting |

