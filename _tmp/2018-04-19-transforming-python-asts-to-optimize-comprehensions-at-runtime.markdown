---
layout: post
title: "Transforming Python ASTs to Optimize Comprehensions"
date: 2018-04-19 17:00:00 -0700
time_to_read: 25-30
has_code: true
redirect_from: writing/transforming_python_asts_to_optimize_comprehensions_at_runtime
---

**tl;dr** Python comprehensions can have duplicate function calls (e.g. `[foo(x) for x in ... if foo(x)]`). If these function calls are expensive, we need to rewrite our comprehensions to avoid the cost of calling them multiple times. In this post, we solve this by writing a decorator that converts a function in to AST, optimizes away duplicate function calls and compiles it at runtime in ~200 lines of code.

<hr>

I _love_ list, dict and set comprehensions in Python. It's the one feature of the language that I feel like I could point at and say "Pythonic". It feels like the [`map`](https://docs.python.org/3/library/functions.html#map) and [`filter`](https://docs.python.org/3/library/functions.html#filter) functions are really baked into the language. More than that, comprehensions stem from [set theory](https://en.wikipedia.org/wiki/Set-builder_notation), so they must be good, right?

In this blog post, I'll briefly describe comprehensions, explain a performance disadvantage that I frequently face, and show you some code that mitigates this disadvantage by transforming them at runtime.

<img src="/assets/imgs/iguana-1.jpeg" alt="An iguana" />

<h3 id="what-are-comprehensions">
  What are comprehensions
</h3>

If you're already familiar with comprehensions, feel free to skip this section! If not, I'll provide a quick breakdown.

Essentially, comprehensions are just syntactic sugar that Python has to, quoting [PEP 202](https://www.python.org/dev/peps/pep-0202/), _"provide a more concise way to create [lists, sets, dictionares] in situations where map() and filter() and/or nested loops would currently be used"_. An example...

{% highlight python %}
# An example of a basic `for` loop in Python
acc = []
for y in range(100):
    if foo(y):
        acc.append(bar(y))

# And here's how you could ~~rewrite~~ simplify the above example using 
# a list comprehension
acc = [bar(y) for y in range(100) if foo(y)]
{% endhighlight %}

The observant Python programmer will also notice that the above can also be rewritten using the built-in `map` and `filter` methods as `map(bar, filter(foo, range(100)))`. Anyway, back to comprehensions...

Comprehensions also allow to you "chain" `for` loops, with latter loops being equivalent to deeper loops. Some more examples...

{% highlight python %}
# This...
acc = []
for y in range(100):
    if foo(y):
        for x in range(y):
            if bar(x):
                acc.append(baz(x))

# ...is semantically equivalent to...
acc = [
    bar(x)
    for y in range(100)
    if foo(y)
    for x in range(y)
    if bar(x)
]

# ...which also provides the same result as...
acc = [
    bar(x)
    for y in range(100)
    for x in range(y)
    if foo(y) and bar(x)
]
{% endhighlight %}


<h3 id="comprehensive-shortcomings">
  Comprehensive shortcomings
</h3>

In my opinion, there's one large shortcoming of comprehensions over their procedural cousins. `for` loops contain statements (e.g. `x = foo(y)`) whereas comprehensions can only contain expressions (e.g. `x + foo(y)`) and are in fact expressions themselves. As a result, we can't alias the return value of a function call so to use it again. This wouldn't be an issue if assignments in Python were treated as expressions (like in C or C++), but they're treated as statements.

{% highlight python %}
# This code calls the function `foo` with arguements `y` twice
acc = []
for y in range(100):
    if foo(y):
        acc.append(foo(y))

# We can rewrite this to make sure `foo` is only called once by assigning
# it's result to a variable and using that instead
acc = []
for y in range(100):
    foo_result = foo(y)
    if foo_result:
        acc.append(foo_result)

# This comprehension calls the function `foo` with arguements `y` twice...
# but we can't rewrite this comprehension in a "clean" way to call `func`
# only once
acc = [foo(y) for y in range(100) if foo(y)]
{% endhighlight %}

This shortcoming really becomes an issue if the `foo` function is expensive. There are some work-arounds to this problem, but I don't like any.

1. We could rewrite the list comprehension as a series of `map` and `filter` function calls.
2. We can cache/memoize the expensive function that we're calling (e.g. using functool's [`lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache) decorator). If the function is in a different module that you don't have access to, you'll have to write a wrapper function and cache the result of the wrapper function. Meh...
3. Or... you can alter your list comprehensions by appending additional `for` loops where their loop invariant work effectively the same as variables. Unfortunately, this makes your comprehension harder to comprehend (\*cough\* \*cough\*) and the whole point of comprehensions is that they're more concise and easier to understand than standard `for` loops. Here's an example:

{% highlight python %}
# We're only calling `foo` once! But we write code for others to read...
acc = [
    foo_result
    for y in range(100)
    for foo_result in [foo(y)]
    if foo_result
]
{% endhighlight %}

<h3 id="lets-build-a-compiler">
  Let's build a compiler!
</h3>

One idea is to take an inefficient, but clean and concise comprehension and optimize away duplicate and equivalent function calls so that it's efficient but ugly (i.e. the 2nd work-around mentioned above). The act of taking a program and rewriting it be quicker while sacrifising clarify is something most compilers do for you, so on the surface this idea doesn't seem unreasonable.

We could build a mini-compiler to do these comprehension transformations before running but since Python is [dynamic](https://en.wikipedia.org/wiki/Dynamic_programming_language), let's do this at runtime! This has a nice advantage of not requiring our users to change their build workflow. We can distribute our comprehension optimization program as a Python module that users can install normally (using [PyPI](https://pypi.python.org/pypi)). Users could just import out module to have it optimize their modules or we could have it using [Python decorators](https://wiki.python.org/moin/PythonDecorators). The latter is slightly more explicit, so we'll start with that!

However, building an end-to-end compiler is hard and is usually broken into [multiple steps](http://www.csd.uwo.ca/~moreno//CS447/Lectures/Introduction.html/node10.html). We really only care about taking an easy-to-manipulate abstract representation of a Python program and manipulating it to be faster.

1. Lexical analysis (or tokenization... or scanning).
2. Syntax analysis (or parsing).
3. Semantic analysis.
4. Intermediate code generation.
5. **Optimization** (this is the only step we really care about).
6. Output code generation.


<h3 id="pythons-ast-module-to-the-rescue">
  Python's <a href="https://docs.python.org/2/library/ast.html"><code class="highlighter-rouge">ast</code></a> module to the rescue!
</h3>

Luckily, Python's standard library has an `ast` module that can take some Python source code as input and produce an [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) (AST). It also provides a [`NodeVisitor`](https://docs.python.org/2/library/ast.html#ast.NodeVisitor) and [`NodeTransformer`](https://docs.python.org/2/library/ast.html#ast.NodeTransformer) that let's us easily walk the structure of a Python program in tree form and transform it as we go. Python also has a built-in [`compile`](https://docs.python.org/2/library/functions.html#compile) function that takes an AST (or string) as input and compiles it into a code object that can then be executed. 

Using this module, it's actually surprisingly easy to write a Python decorator that accesses the wrapped function's source code, converts it to an AST, transforms it, compiles it and returns that newly compiled function. We'll call the decorator `@optimize_comprehensions` for fun.

{% highlight python %}
def optimize_comprehensions(func):
    source = inspect.getsource(func)
    in_node = parse(source)
    # TODO: Implement OptimizeComprehensions
    out_node = OptimizeComprehensions().visit(in_node)
    new_func_name = out_node.body[0].name
    func_scope = func.__globals__
    # Compile the new method in the old methods scope. If we don't change the
    # name, this actually overrides the old function with the new one
    exec(compile(out_node, '<string>', 'exec'), func_scope)
    return func_scope[new_func_name]


# Example usage
@optimize_comprehensions
def basic_list_comprehension(expensive_func):
    return [
        expensive_func(x)
        for x in range(100)
        if expensive_func(x)
    ]
{% endhighlight %}

The grammar for the AST is described in the [Abstract Syntax Description Language](https://docs.python.org/2/library/ast.html#abstract-grammar) (ASDL). Here's the description of the `ListComp`, `SetComp` and `DictComp` nodes. I've also included the `GeneratorExp` node since it has a very similar syntactic structure to comphrensions and we can apply the same optimizations to it. I've also included the description of function call (`Call`) nodes as we'll be optimizating out duplicates of those.

{% highlight python %}
expr = ...
     | ListComp(expr elt, comprehension* generators)
     | SetComp(expr elt, comprehension* generators)
     | DictComp(expr key, expr value, comprehension* generators)
     | GeneratorExp(expr elt, comprehension* generators)
       ...
     | Call(expr func, expr* args, keyword* keywords,
            expr? starargs, expr? kwargs)

comprehension = (expr target, expr iter, expr* ifs)
{% endhighlight %}

#### Removing the function decorator (or preventing infinite recursion) ####

If we're not careful, since we're performing optimizations at runtime, we may perform these optimizations every time our function (the one wrapped with `@optimize_comprehensions` decorator) is called. Moreover, this would actually cause users to infinitely recurse when they attempt to call the function to be optimized.

To prevent this, the first transformation we'll perform is to remove the decorator from our function. We'll do this by removing any decorators from the function with the name `optimize_comprehensions`. This is by far the simplest solution so we'll go with it, but it doesn't actually work if user renamed the decorator when importing it (i.e. `from optimize_comprehensions import optimize_comprehensions as oc`) or if the user namespaced their decorator by importing the module (i.e. `import optimize_comprehensions`).


{% highlight python %}
    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        # Remove the fast_comprehensions decorator from the method so we
        # don't infinitely recurse and/or attempt to re-optimize the node
        decorators = node.decorator_list
        node.decorator_list = [
            decorator
            for decorator in node.decorator_list
            if decorator.id != 'optimize_comprehensions'
        ]
        return node
{% endhighlight %}

#### Equivalent function calls ####

To determine if a there are duplicte function calls, we must first define an equality relation between `Call` nodes. We could make this super smart by ingorning ordering of keyword arguments (e.g. `foo(a=1, b=2) == foo(b=2, a=1)`) and evaluating arguement expressions to determine if their result is equal (e.g. `foo(a=1+2) == foo(a=3)`). However, for the sake of simplicity, we'll just say two `Call` nodes are equal if they had the same "formatted dump" (essentially,  the same string representation) using the `dump` method.

#### Finding duplicate function calls ####

Our `OptimizeComprehensions` `NodeTransformer` will work by walking the subtree of comprehension (or generator) node and relacing duplicate `Call` nodes with a `Name` node that will read the value that a variable points to. In order to do this, we must first do a initial pass over the subtree of a comprehension and find duplicate nodes. We'll acheive this by creating a `NodeVisitor` class that will visit `Call` nodes and take return duplicate `Calls`.


{% highlight python %}
class DuplicateCallFinder(NodeVisitor):
    calls = {}

    def visit_Call(self, call):
        call_hash = dump(call)
        _, current_count = self.calls.get(call_hash, (call, 0))
        self.calls[call_hash] = (call, current_count + 1)

    @property
    def duplicate_calls(self):
        return [
            call
            for _, (call, call_count) in self.calls.items()
            if call_count > 1
        ]


class OptimizeComprehensions(NodeTransformer):
    calls_to_replace_stack = []

    def visit_comp(self, node):
        # Find all functions that are called multiple times with the same
        # arguments as we will replace them with one variable
        call_visitor = DuplicateCallFinder()
        call_visitor.visit(node)

        # Keep track of what calls we need to replace using a stack so we
        # support nested comprehensions
        self.calls_to_replace_stack.append(call_visitor.duplicate_calls)

        # TODO: Replace all duplicate calls with a variable and new
        # comprehensions to the list of comprehensions with the variable and
        # function call

        # Make sure we clear the calls to replace so we don't replace other
        # calls outside of the scope of this current list comprehension
        self.calls_to_replace_stack.pop()
        return node

    # Optimize list, set and dict comps, and generators the same way
    visit_ListComp     = visit_comp
    visit_SetComp      = visit_comp
    visit_DictComp     = visit_comp
    visit_GeneratorExp = visit_comp
{% endhighlight %}

#### Replacing duplicate calls with variables

The next step is to replace each duplicate `Call` node with a `Name` node. In Python terms, this means replacing duplicate function calls with variables.

<img src="/assets/imgs/iguana-2.jpeg" alt="Another iguana" />

This is fairly trivial, but there is one decision we have to make. How do we generate variable names from a function call? I've chosen a simple but ugly solution: hash the formatted function dump and prepend it with double underscores (as Python variable names cannot start with numbers). If we were to inspect our transformed comprehension, we may see variables that look like `__258792`. This solution is "ugly" as it's vulnerable to hash collisions. However, for the purpose of this blog post, we're going to pretend they don't exist.

{% highlight python %}
    def visit_Call(self, node):
        # Flatten the stack of calls to replace
        call_hashes = [
            dump(call)
            for calls_to_replace in self.calls_to_replace_stack
            for call in calls_to_replace
        ]
        # If we should replace the Call, replace it with a Name node
        if dump(node) in call_hashes:
            name_node = Name(id=self._identifier_from_Call(node), ctx=Load())
            # Add linenos and other things the compiler needs to the new node
            fix_missing_locations(name_node)
            return name_node

        return node

    def _identifier_from_Call(self, node):
        return '__{}'.format(abs(hash(dump(node))))
{% endhighlight %}

#### Moving the function call to a new "comprehension" ####

Now that we're using variables (`Name` nodes) instead of duplicate function calls (`Call` nodes), we must make sure we assign the result of the function calls to the new variables. We do this by adding another `comprehension` to the `ListComp`, `SetComp`, `DictComp` or `GeneratorExp` node's list of `comprehension`s that looks like `for __256792 in [foo(y)]`.

However, if we reference the ASDL, we'll see that the description of a `comprehension` is `(expr target, expr iter, expr* ifs)`, which put plainly means that `comprehension`s contain `if` statements. If we leave these `if` statements as is (or is it "as are"?) _and_ if we append the new `comprehension`s to the end of the list of `comprehension`s, we'll have issues looking up new variables before they're defined. Consider the following example:


{% highlight python %}
# This comprehension ...
[
    foo(y)
    for y in range(100)
    if foo(y) % 2
]

# ... would be optimized into ...
[
    __258792
    for y in range(100)
    if __258792 % 2             # __258792 isn't defined! Exception!
    for __258792 in [foo(y)]    # Now it's defined, but too late!
]
{% endhighlight %}

One solution would be to be very smart about our placement of new `comprehension`s such that they're always placed before any uses of the new variable. A simpler, but less efficient solution is to just move all `if` statements to the last `comprehension` in the list of `comprehension`s. This is less efficient as `if` statements interleaved with `for` loop statements allow us to break out of loops faster. We'll go with the latter solution for the sake of this blog post, but it's not the ideal solution.

This is what our `visit_comp` method looks like now:

{% highlight python %}
    def visit_comp(self, node):
        # ...
        # Visit children of this list comprehension and replace calls
        self.generic_visit(node)

        # Gather the existing if statements as we need to move them to the
        # last comprehension generator (or there will be issues looking up
        # identifiers)
        existing_ifs = []
        for generator in node.generators:
            existing_ifs += generator.ifs
            generator.ifs = []

        # Create a new for loop for each function call result that we want
        # to alias and add it to the list comprehension
        for call in call_visitor.duplicate_calls:
            new_comprehension = comprehension(
                # Notice that we're storing (Store) the result of the call
                # instead of loading it (Load)
                target=Name(
                    id=self._identifier_from_Call(call),
                    ctx=Store()
                ),
                iter=List(elts=[call], ctx=Load()),
                ifs=[],
                is_async=0,
            )
            # Add linenos and other things the compile needs to node
            fix_missing_locations(new_comprehension)
            node.generators.append(new_comprehension)

        node.generators[-1].ifs = existing_ifs
        # ...
{% endhighlight %}

#### Unique target variable names ####

Our optimizer is nearly there. It currently fails when a nested comprehension has the target variable name as another child comprehension within the same top level comprehension (it also fails if it has the same target variable name as the top level comprehension). So what's the solution? Another stupidily simple solution that is to change the name of all target variable names that are children of a comprehension node so that they're unique.

To make variable names unique, I've decided to append random numbers to the end of variable names. This also suffers from naming conflicts, but for the purpose of this blog post, it'll do. We'll also use a stack of variable names to replace, similar to what we did with the `calls_to_replace_stack` in the `OptimizeComprehensions` `NodeTransformer` to keep track of scope.

Here's an example implementation of a `NodeTransformer` that renames variable names in comprehensions. You'll notice we only need to call it once within our `OptimizeComprehensions`.

{% highlight python %}
class RenameTargetVariableNames(NodeTransformer):
    variables_to_replace_stack = []

    def visit_comp(self, node):
        # Visit all of the comprehensions in the node and make sure to add
        # the target variable names to the stack of variable names to
        # replace.
        for generator in node.generators:
            self.visit(generator.iter)
            self.variables_to_replace_stack.append(dict())
            self.visit(generator.target)
            for _if in generator.ifs:
                self.visit(_if)

        # Visit the output expression in the comprehension
        if isinstance(node, DictComp):
            self.visit(node.key)
            self.visit(node.value)
        else:
            self.visit(node.elt)

        # Make sure we pop the variables off the stack of variable names
        # to replace so we don't continue to replace variable names 
        # outside of the scope of the current comprehension
        self.variables_to_replace_stack[:-len(node.generators)]
        return node

    def visit_Name(self, node):
        # Assignments to target varibles in a comprehension (if the stack
        # is empty, we're not in a comprehension)
        if isinstance(node.ctx, Store) and self.variables_to_replace_stack:
            random_int = randint(0, maxsize)
            new_id = f'{node.id}__{random_int}'
            self.variables_to_replace_stack[-1][node.id] = new_id
            node.id = new_id

        # Loading the value of target varibles in a comprehension (if the
        # stack is empty, we're not in a comprehension)
        elif isinstance(node.ctx, Load) and self.variables_to_replace_stack:
            flattened_variables_to_replace = {}
            for variables_to_replace in self.variables_to_replace_stack:
                flattened_variables_to_replace.update(variables_to_replace)

            if node.id in flattened_variables_to_replace:
                node.id = flattened_variables_to_replace[node.id]
        return node
{% endhighlight %}

Another thing to note is that we push a map of variables to replace for each comprehension in a comprehension node's generators. By doing so, we can handle the case where we re-assign target variable names across generators within the same comprehension node. For example, the following test case passes.

{% highlight python %}
@optimize_comprehensions
def multiple_generators_with_same_target_variable_name(expensive_func):
    return [
        (expensive_func(x), x)
        for x in [2]
        if expensive_func(x)
        for x in [x * x]
        if expensive_func(x)
    ]

def test_multiple_generators_with_same_target_variable_name():
    expensive_func = mock.Mock(return_value=True)
    assert multiple_generators_with_same_target_variable_name(
        expensive_func,
    ) == [(True, 4)]
    expensive_func.assert_has_calls(
        calls=[mock.call(2), mock.call(4)],
        any_order=True,
    )
{% endhighlight %}


<h3 id="to-conclude-weve-done-it">
  To conclude, we've done it!
</h3>

In 200 lines of Python (including docstrings, comments and imports), we've built an optimizer that takes potentially slow but elegant comprehensions and produces ugly but fast comprehensions at runtime.

For simple comprehensions with a duplicate function call, the execution time of our optimized version converges to half the execution time of the original, as the time it takes to execute the function increases. The line chart below illustrates this statement and was generated by comparing the execution time of list comprehension before and after optimization (see [GitHub gist](https://gist.github.com/mikeecb/d21dab6fb9f8632ec10e18bcbabd3219) for script).

<img src="/assets/imgs/comprehension-graph.svg" alt="A graph comparing the execution time of list comprehensions before and after optimization" />

Anyway, I hope you've enjoyed reading this walk-through and here's a [GitHub gist](https://gist.github.com/mikeecb/4a310051840c96a237204045243419db) of the optimzer code we've gone through! Feel free to run it, modify it and distribute it. I may polish it up one day and publish to PyPI for all to use.

Some takeaways:

1. Writing a code optimizer is generally pretty simple, especially with Python's `ast` module. Go ahead and try!
2. You can _never_ trust the Python code you're calling... even if you have the source code (which you almost always have access to when working with Python). If someone can inject some malicious code into your Python process, they now have entire control of it.

#### Caveats ####

Writing optimizers and/or compilers has the potential of creating really-hard-to-debug bugs. Although this has been a fun exercise, I don't recommend using the optimizer written in this post at the moment in any production environments.

It's also important to properly trace and profile code before applying optimizations like the ones above. Runtime optimizations incur overhead and may actually slow down code instead of speeding it up. For example, our optimizer only works if the overhead of transforming functions is lower than the overhead of executing duplicate function calls.

<hr/>

**Update** (August 11, 2018): I thought I would add, [PEP 572](https://www.python.org/dev/peps/pep-0572/) introduces assigment expressions to Python with the new `:=` operator! This solves the comprehension issue described in this post, but this should still be a helpful guide on how to use the `ast` module to transform Python programs at runtime!
