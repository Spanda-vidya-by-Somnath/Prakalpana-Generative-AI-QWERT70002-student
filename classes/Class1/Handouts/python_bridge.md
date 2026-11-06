# Python for programmers: a bridge

You already program in another language. This page shows the Python you will meet in the course scripts,
next to JavaScript, Ruby and Java. Read it once, then keep it open during labs. Anything not here: ask your AI assistant
"What does this line do? Show me the equivalent in <your language>."

## The ten differences that matter

| | Python | JavaScript | Ruby | Java |
|---|---|---|---|---|
| Blocks | indentation (4 spaces) + `:` | `{ }` | `do … end` | `{ }` |
| Variable | `x = 5` | `let x = 5` | `x = 5` | `int x = 5;` |
| String formatting | `f"Hi {name}"` | `` `Hi ${name}` `` | `"Hi #{name}"` | `"Hi " + name` |
| Nothing | `None` | `null` / `undefined` | `nil` | `null` |
| Booleans | `True` / `False` | `true` / `false` | `true` / `false` | `true` / `false` |
| List / array | `[1, 2, 3]` | `[1, 2, 3]` | `[1, 2, 3]` | `List.of(1, 2, 3)` |
| Dictionary / map | `{"a": 1}` | `{a: 1}` | `{a: 1}` / `{"a" => 1}` | `Map.of("a", 1)` |
| Function | `def f(x):` | `function f(x) {` | `def f(x)` | `int f(int x) {` |
| Logic | `and` `or` `not` | `&&` `\|\|` `!` | `&&` `\|\|` `!` | `&&` `\|\|` `!` |
| Comment | `# ...` | `// ...` | `# ...` | `// ...` |

## Side by side

```python
# Python
def greet(name: str, times: int = 1) -> str:      # type hints are optional, not enforced
    return " ".join([f"Hi {name}!"] * times)

people = ["Asha", "Ravi"]
for p in people:
    print(greet(p))

ages = {"Asha": 31, "Ravi": 27}
adults = [n for n, a in ages.items() if a >= 18]   # list comprehension = map + filter
```

```ruby
# Ruby
def greet(name, times = 1) = (["Hi #{name}!"] * times).join(" ")
people = ["Asha", "Ravi"]
people.each { |p| puts greet(p) }
ages = { "Asha" => 31, "Ravi" => 27 }
adults = ages.select { |_, a| a >= 18 }.keys
```

```javascript
// JavaScript
const greet = (name, times = 1) => Array(times).fill(`Hi ${name}!`).join(" ");
const people = ["Asha", "Ravi"];
for (const p of people) console.log(greet(p));
const ages = { Asha: 31, Ravi: 27 };
const adults = Object.entries(ages).filter(([, a]) => a >= 18).map(([n]) => n);
```

## What you'll see in the course code

| Python | Meaning |
|---|---|
| `from llm import ask` | import one name from the file `llm.py` (like `require` / `import`) |
| `reply = ask("Hi", system="Be brief")` | keyword arguments: named parameters, in any order |
| `reply.text`, `reply.usage_line()` | attribute and method of an object |
| `with open("f.txt") as f:` | open, use, and always close (like a `try … finally`) |
| `@dataclass class Reply:` / `class City(BaseModel):` | a class whose fields are declared, not written in a constructor |
| `for i, doc in enumerate(docs):` | loop with an index |
| `x = a if cond else b` | the ternary `cond ? a : b` |
| `try: … except ValueError as e:` | `try … catch` |
| `**kw`, `*args` | "the rest of the keyword / positional arguments" |
| `QUESTION = "…"  # change me` | a value you are meant to change and run again |
| `# %%` | starts a cell: VS Code shows **Run Cell** above it |

## Gotchas

- **Indentation is syntax.** Mixing tabs and spaces breaks code. Let the editor indent.
- **`=` copies the reference**, not the list: `b = a` then `b.append(1)` changes `a` too. Use `b = a.copy()`.
- **Integer division:** `7 / 2` is `3.5`; `7 // 2` is `3`.
- **Default arguments are created once:** never write `def f(x=[])`.
- **Strings are immutable**; `s.upper()` returns a new string.
