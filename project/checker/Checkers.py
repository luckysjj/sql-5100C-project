from DB import *
from Config import config
from Utilities import *
from Expected import *
from Answer import *

"""
Log Print
0: Print All
1: Print Trace
2: Print Important
3: No Print
"""
LOG_LEVEL = 1
def log(level, *msg):
  if level >= LOG_LEVEL:
    print(*msg)

def info(qns):
  if 1 <= qns <= len(exps):
    idx = qns - 1
    log(3, table(*exps[idx]))

"""
Helper
"""
def check_header(act, exp):
  if exp != None:
    if len(act) != len(exp):
      return (False, f'''Header: Different Size
  Actual: {len(act)}
  Expect: {len(exp)}
''')
    else:
      res = ''
      check = []
      res += 'Header: Same Size\n'
      valid = True
      for i in range(len(act)):
        if act[i] != exp[i]:
          valid = False
        check.append(('✓' if act[i] == exp[i] else '✗', act[i], exp[i]))
      res += table(['Result', 'Actual', 'Expect'], check)
      return (valid, res)
  else:
    return (True, '')

def compare(set1, set2, head, title):
  return f'''{title}
{table(head, list(set1 - set2))}

'''

def check_body(act, exp, head):
  a0 = len(act[0]) if len(act) > 0 else -1
  e0 = len(exp[0]) if len(exp) > 0 else -1

  if a0 >= 0 and e0 >= 0 and a0 != e0:
    return f'''Mismatch Header Size
  Actual: {a0}
  Expect: {e0}
'''
  
  acts = set(act)
  exps = set(exp)
  return f'''Body
  Actual: {len(act)}
  Expect: {len(exp)}

{compare(acts, exps, head, "Extra")}

{compare(exps, acts, head, "Missing")}
'''

def diff(act, exp):
  n, m = len(act), len(exp)
  def lev(i, j):
    if i == n:
      return list(map(lambda row: ('-', row), exp[j:]))
    if j == m:
      return list(map(lambda row: ('+', row), act[i:]))
    if act[i] == exp[j]:
      return [('✓', exp[j])] + lev(i + 1, j + 1)
    _exp = [('-', exp[j])] + lev(i, j + 1)
    _act = [('+', act[i])] + lev(i + 1, j)

    if len(_exp) < len(_act):
      return _exp
    else:
      return _act
  return lev(0, 0)
  

"""
Execution Checker
"""
# Unordered Comparison with optional header
def unordered(sql, body, head = None):
  act = DB(**config).fetch(sql).close().res

  if len(act) == 0:
    log(1, 'Unable to execute')
    return (False, False)
  if len(act) > 1:
    log(1, 'Multiple statement detected')
    return (False, False)
  
  # Check error
  if isinstance(act[0], Exception):
    log(1, repr(act[0]))
    return (False, False)

  # Retrieve actual result
  _head, _body = act[0]
  hd, hdlog = check_header(_head, head)
  log(1, hdlog)
  log(1, check_body(_body, body, _head))

  _sbody, sbody = set(_body), set(body)
  return (hd, len(_body) == len(body) and _sbody == sbody)

# Ordered Comparison with optional header
# - Ordering result displayed using 'diff'
# - Computed with Levenshtein distance
#   on table
def ordered(sql, body, head = None):
  act = DB(**config).fetch(sql).close().res
  
  if len(act) == 0:
    log(1, 'Unable to execute')
    return (False, False)
  if len(act) > 1:
    log(1, 'Multiple statement detected')
    return (False, False)

  # Check error
  if isinstance(act[0], Exception):
    log(1, repr(act[0]))
    return (False, False)

  # Retrieve actual result
  _head, _body = act[0]
  res = ''
  hd, hdlog = check_header(_head, head)
  log(1, hdlog)
  log(1, check_body(_body, body, _head))
  log(1, 'Ordered Diff')
  log(1, table(['#'] + _head,
               list(map(lambda row: (row[0],) + row[1],
                        diff(_body, body)))))
  
  return (hd, _body == body)


"""
Tester
"""
_TESTER = [unordered, ordered]
def test(qns):
  idx = qns - 1
  log(0, f'''Running SQL
{ans[idx]}
''')
  hd, bd = _TESTER[ords[idx]](ans[idx], exps[idx][1], exps[idx][0])
  log(2, f'Qn {qns}: Header = {"✓" if hd else "✗"} ; Body = {"✓" if bd else "✗"}')
  return (hd, bd)
  
def test_all():
  tbl = []
  for qns in range(1, len(exps) + 1):
    hd, bd = test(qns)
    tbl.append((qns, "✓" if hd else "✗", "✓" if bd else "✗"))
  log(3, table(('qns', 'header', 'body'), tbl))


# Display the result as a table
def display(qns):
  idx = qns - 1
  sql = ans[idx]
  res = DB(**config).fetch(sql).close().res[-1]
  print(table(res[0], res[1]))

def expected(qns):
  idx = qns - 1
  exp = exps[idx]
  print(table(*exp))


test_all()
