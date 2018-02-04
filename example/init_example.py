
# This is an example of a python file you might create to serve as an implementation store


# If no provider is used, then no need to include an argument.
def fun_zero(x):
    print(x)


def fun_hello():
    print("Hello")


# Note that the first argument for a function should be a provider, if function takes a provider. Note
#   that if you include a provider argument, you must specify pass_provider=True
def f_set(provider, key, value):
    provider.set(key, value)
    print('%s set to %s' % (key, value))


def f_get(provider, key):
    value = provider.get(key)
    print("%s: %s" % (key, value))


def f_inc(provider, key):
    value = int(provider.get(key)) + 1
    provider.set(key, value)
    print("%s: %s (incremented)" % (key, value))


def fun_three(provider):
    x = provider.get('x')
    print("x: %d" % x)


def con_less(provider, key, max):
    value = int(provider.get(key))
    return value < max

# By convention (and if you want the TextCommunicator to interact correctly) include all your function
#   primitives in the variable 'fn_dict' and give the store name in 'fn_store_name'
fn_dict = {'fun_zero': fun_zero, 'fun_hello': fun_hello, 'fun_set': f_set, 'fun_get': f_get,
           'fun_3': fun_three, 'inc': f_inc, 'less': con_less}
fn_store_name = 'example_store'
