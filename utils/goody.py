# These names are meant to be imported like:
#   from goody import irange
# or
#   import goody
#     which would be used as goody.irange


def type_as_str(x):
    """
    Returns the type of x as a nice string
    For example: type(a) returns "<class 'xxxxxxxx'>; this function extracts the
      'xxxxxxx' part: the first ' is at index 8; the last ' is at index -2
    """
    return str(type(x))[8:-2]


class ProtocolError(Exception):
    pass

def implements_protocol(entity, protocol : [str]) -> bool:
    """
    Checks whether an object or a class implements all the methods in a protocol
    Each method must be callable (a predicated applied to the retrieved attribute)
    """
    try:
        return all(callable(getattr(entity,attr)) for attr in protocol)
    except:
        return False # getattr raised exception: attr not found


def irange(*args):
    """
    Returns an inclusive range: e.g., for i in irange(1,10): print(i)
      prints the numbers 1 through 10 inclusive
    Use it like range (with 1, 2, or 3 arguments), but with irange the stop
      value is in the range
    """
    if len(args) == 1:
        return range(1,args[0]+1)
    if len(args) == 2:
        return range(args[0],args[1]+1)
    if len(args) == 3:
        return range(args[0],args[1]+(1 if args[2]>0 else -1),args[2])
    raise TypeError('irange expected 1-3 arguments, got ' + str(len(args)))
 
 
def frange(*args):
    """
    Returns a float range: e.g., for i in range(0.1, 1.0, 0.1): print(i)
      prints the numbers .1, .2, .3, ... .9, 1.: 0.1 through 1.0 inclusive
    Use it like range/irange (with 1, 2, or 3 arguments).
    """
    start = 0.
    step  = 1.
    if len(args) == 1:
        stop = args[0]
    elif len(args) == 2:
        start,stop = args[0],args[1]
    elif len(args) == 3:
        start,stop,step = args[0],args[1],args[2]
    else:
        raise TypeError('frange expected 1-3 arguments, got ' + str(len(args)))
    if step == 0.:
        raise ValueError('frange step cannot be 0.')
    i = 0
    while True:
        curr = start + i*step
        if (step > 0. and curr > stop+.1*step) or (step < 0. and curr < stop-.1*step):
            return
        yield curr
        i += 1


def leading(text,c=' ',extra=0):
    """
    Returns a string of all c, whose length is the # of c's at the front of text
      e.g., leading('xxxyy','x') returns 'xxx'
    """
    for i in range(0,len(text)):
        if text[i] != c:
            return (i+extra)*c
    return text


def safe_open(prompt_text,mode,error_message,default=''):
    """
    Prompts the user for a file (openable in mode) with and error message
      to display if opening the file in that mode fails)
    If mode=='w', and the file exists, the user will be prompted whether to overwrite it
    If default is supplied, it will appear in the prompt and be the file
      opened if the user just presses enter
    """
    import prompt
    default = str(default) # ensure default is a string
    while True:
        try:
            file_name = input(prompt_text + ('' if default == '' else '['+default+"]") + ": ")
            if file_name == '':
                file_name = default
            try:
                if mode == 'w' and open(file_name,'r'):
                    if not prompt.for_bool(leading(prompt_text,extra=2) + 'File exists: overwrite',False):
                        continue
            except IOError:
                pass
            file = open(file_name,mode)
            return file
        except IOError:
            print(leading(prompt_text,extra=2) + 'Tried file: \''+file_name+'\': ' + error_message) 


def parse_lines(open_file, sep, conversions):
    """
    Iterator for reading values a line at a time from an open file; the line's
      items are strings separated by the character that is the sep parameter.
    Each item/string has its own (positional) conversion function called on it.
    Example: iterating over read_file_values(file, ' ', [str,int,int]) 
      produces a 3-tuple for each line, containing a string, int, and int.
    So, the line
      abc 12 34
    yields the list ['abc', 12, 34]
    """
    for line in open_file:
        yield [conv(item) for conv,item in
                  zip(conversions,line.rstrip('\n').split(sep))]