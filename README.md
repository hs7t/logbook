# logbook

logbook is simple software that lets you log and tag events - as if you were 
a computer!

## Using logbook

> [!TIP]
> You can add `--help` to the end of any command to get more info about it.

### Writing to your logbook

Logbook lets you write logs, like this:

```bash
logbook write "Forgot my keys"
```

Isn't that cool? You can also assign *tags* to them:

```bash
logbook write "Ate hotdog" --tag life
logbook write "Forgot my keys" --tag lostitems
```

Tags can have *states*: a tag's state is like a counter you add to and 
substract from. You can change a state's value using a modifier, like this:

```bash
logbook write "Forgot my keys" -t lostitems +1
```

...or like this:

```bash
logbook write "Stressed out because of exams" -t willtolive -10
```

### Reading from your logbook

#### `read logs`

After writing some stuff to your logbook, you probably want to read it. To 
get a table with the logs you've written, do:

```bash
logbook read logs
```

By default, `read logs` will only show your 10 most recent logs. You can change
this:

```bash
logbook read logs 15    # will show 15 logs
```

There's some arguments you can use to customize the `read logs` output:

```bash
logbook read logs -t willtolive -t lostitems    # shows all logs that have 'willtolive' or 'lostitems' for tags
logbook read logs --sort tag    # sort items by their tag
logbook read logs --ascending   # output in ascending order
```

#### `read tags`

To get a nice overview of all tags (and their states), do:

```bash
logbook read tags
```
### Setting things up with `config`

#### `tag create`

`logbook` will try to be helpful and add tags for you automatically. If you
ever want to add tags yourself, you can do something like this:

```bash
logbook config tag create lostitems   # creates a new tag called lostitems
```

By default, that'll create a static (i.e. stateless) tag. You can make your new
tag a stateful one like so:

```bash
logbook config tag create lostitems --tag-kind stateful
```

#### `tag delete`

If you don't want a tag anymore, you can delete it:

```bash
logbook config tag delete carsseen  # deletes the tag 'carsseen'
```

Of course, your old logs assigned to this tag will need to be updated! You can 
choose what happens to them via the prompts `logbook` will give you.