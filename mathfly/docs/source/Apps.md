# Mathfly application support

## Sumatra pdf
| Voice command         | Keystroke           |
|:----------------------|:--------------------|
| `open file`           | `c-o`               |
| `print file`          | `c-p`               |
| `close tab`           | `c-w`               |
| `next tab`            | `c-tab`             |
| `previous tab`        | `cs-tab`            |
| `<nth> tab`           | `a-%(nth)s`         |
| `go to page`          | `c-g`               |
| `find`                | `c-f`               |
| `find next`           | `f3`                |
| `find previous`       | `s-f3`              |
| `page <n>`            | `c-g, %(n)s, enter` |
| `table of contents`   | `f12`               |
| `zoom in`             | `c-equals`          |
| `zoom out`            | `c-minus`           |
| `fit page`            | `c-0`               |
| `actual size`         | `c-1`               |
| `fit width`           | `c-2`               |
| `fit content`         | `c-3`               |
| `[view] single page`  | `c-6`               |
| `facing view`         | `c-7`               |
| `book view`           | `c-8`               |
| `rotate [right]`      | `c-plus`            |
| `rotate left`         | `c-minus`           |
| `presentation [mode]` | `f11`               |
| `full screen`         | `s-f11`             |

## Wordpad
| Voice command     | Keystroke        |
|:------------------|:-----------------|
| `new file`        | `c-n`            |
| `open file`       | `c-o`            |
| `print file`      | `c-p`            |
| `page down [<n>]` | `c-pagedown * n` |
| `page up [<n>]`   | `c-pageup * n`   |


## Sublime text
| Voice command                                       | Keystroke                      |
|:----------------------------------------------------|:-------------------------------|
| `new (file / pane)`                                 | `c-n`                          |
| `new window*`                                        | `ca-n`                         |
| `open file`                                         | `c-o`                          |
| `open folder*`                                       | `cs-o`                         |
| `save as`                                           | `cs-s`                         |
| `comment line`                                      | `c-slash`                      |
| `comment (block / lines)`                           | `cs-slash`                     |
| `outdent lines`                                     | `c-lbracket`                   |
| `join lines [<n3>]`                                 | `c-j`                          |
| `match bracket`                                     | `c-m`                          |
| `(select / sell) scope [<n2>]`                      | `cs-space`                     |
| `(select / sell) brackets [<n2>]`                   | `cs-m`                         |
| `(select / sell) line [<n2>]`                       | `c-l`                          |
| `(select / sell) indent`                            | `cs-j`                         |
| `(select / sell) paragraph*`                         | `ca-p`                         |
| `toggle side bar`                                   | `c-k, c-b`                     |
| `find`                                              | `c-f`                          |
| `get all`                                           | `a-enter`                      |
| `replace`                                           | `c-h`                          |
| `edit lines`                                        | `cs-l`                         |
| `edit next [<n3>]`                                  | `c-d`                          |
| `edit skip next [<n3>]`                             | `c-k, c-d`                     |
| `edit all`                                          | `c-d, a-f3`                    |
| `transform upper`                                   | `c-k, c-u`                     |
| `transform lower`                                   | `c-k, c-l`                     |
| `transform title*`                                   | `c-k, c-t`                     |
| `line <n11> [<n12>]`                                | `c-g, %(n11)s, %(n12)s, enter` |
| `go to file`                                        | `c-p`                          |
| `go to word`                                        | `c-semicolon`                  |
| `go to symbol`                                      | `c-r`                          |
| `go to [symbol in] project`                         | `cs-r`                         |
| `command pallette`                                  | `cs-p`                         |
| `(find / search) in (project / folder / directory)` | `cs-f`                         |
| `fold`                                              | `cs-lbracket`                  |
| `unfold`                                            | `cs-rbracket`                  |
| `unfold all`                                        | `c-k, c-j`                     |
| `fold [level] <n2>`                                 | `c-k, c-%(n2)s`                |
| `full screen`                                       | `f11`                          |
| `(set / add) bookmark`                              | `c-f2`                         |
| `next bookmark`                                     | `f2`                           |
| `previous bookmark`                                 | `s-f2`                         |
| `clear bookmarks`                                   | `cs-f2`                        |
| `build it`                                          | `c-b`                          |
| `record macro`                                      | `c-q`                          |
| `play [back] macro [<n3>]`                          | `cs-q`                         |
| `(new / create) snippet`                            | `a-n`                          |
| `close tab`                                         | `c-w`                          |
| `next tab`                                          | `c-pgdown`                     |
| `previous tab`                                      | `c-pgup`                       |
| `<nth> tab`                                         | `a-%(n2)s`                     |
| `column <cols>`                                     | `as-%(cols)s`                  |
| `focus <panel>`                                     | `c-%(panel)s`                  |
| `move <panel>`                                      | `cs-%(panel)s`                 |
| `split right*`                                       | `as-2, c-1, ca-v, cs-2`        |
| `open terminal`                                     | `cs-t`                         |
| `zoom in [<n2>]`                                    | `c-equal * n2`                 |
| `zoom out [<n2>]`                                   | `c-minus * n2`                 |

\* Commands marked with an asterisk require changes to the user key bindings to work.
Adding the following to preferences->key bindings will allow them to work.
```
{"keys": ["ctrl+alt+n"], "command": "new_window"},                   
{"keys": ["ctrl+shift+o"], "command": "prompt_add_folder"},          
{"keys": ["ctrl+alt+p"], "command": "expand_selection_to_paragraph"},
{"keys": ["ctrl+k", "ctrl+t"], "command": "title_case"},             
{"keys": ["ctrl+alt+v"], "command": "clone_file"}                    
```

## Creating new rules