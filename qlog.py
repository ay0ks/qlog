import inspect
import logging
import time
import datetime
import sys

import rich.pretty

from dataclasses import dataclass

from rich import print

__all__ = ["QLogId", "QLevel", "QLog", "QExceptionHandler"]

pad=lambda a,b,c,d,e:((f:=int((b-len(a))/2)),dict(center=f"{' '*d}{' '*f}{a}{' '*f}{' '*e}",left=f"{' '*d}{a}{' '*f}{' '*e}",right=f"{' '*d}{' '*f}{a}{' '*e}")[c])[1]

DATE_FORMATS={"short": "%D",
              "normal": "%Y-%m-%d %H:%M:%S",
              "long": "%Y-%m-%d %H:%M:%S.%s %P"}
_QLOG_TRACEBACK="rich" #"custom"

def unwrap_b(b):
  try:return b.__dict__
  except:return b

@dataclass
class QLogId:
  id: int
  name: str

class QLevel:
  Notset=-2
  Debug=-1
  Trace=0
  Info=1
  Warn=2
  Error=3
  Critical=4

class QLog:
  def __init__(self,**_X:"initializer arguments"):
                     #_X0:"minimum level"=QLevel.Info,
                     #_X1:"date type or status"="normal",
                     #_X2:"date format"=None
    self._C0,self._C1=(_X.get("log_level",QLevel.Notset),_X.get("date","normal"))
    match self._C1:
      case "custom":self._C3=_X.get("date_format",None)
      case None:self._C3=""
      case _:self._C3=DATE_FORMATS[self._C1]

  def _log_base(self,_X0:"target logger",
                     _X1:"message to log",
                     _X2:"text ansi filter",
                     _X3:"infoblock color",
                     _X4:"print function"=print):
    _X5:"current frame"=inspect.currentframe()
    _X6:"function callee"=inspect.getouterframes(_X5,2)
    if QLevel().__getattribute__(_X6[1][3].title())>=self._C0:
      _X7:"log date format"=self._C3
      _0:"date"=datetime.datetime.now().strftime(_X7)
      _01:"date string"=f"{_0} "if self._C1 is not None and self._C3 is not None else""
      _1:"color"=_X3
      _2:"padded id"=pad(f"{_X0.id}",len(f"{_X0.id}")+3,"left",1,0)
      _3:"padded name"=pad(_X0.name,len(f"{_X0.name}")+3,"right",1,1)
      _4:"infoblock"=f"[{_2}/{_3}]"
      _5:"message"=_X1
      _6:"message filter"=_X2
      print(f"[{_6}]{_01}[{_1}]{_4}[/] {_5}")
  def log(self,_X0:"target logger",
               _X1:"message to log"):
    _1:"loglevel"=self._C0
    _2:"color"={-2:"dim",
                -1:"purple",
                 0:"magenta",
                 1:"blue",
                 2:"yellow",
                 3:"dark_red",
                 4:"red"}[_1]
    _3:"message filter"="dim"if _1=="DEBUG"else"normal"
    self._log_base(_X0,_X1,_3,_3)
  def notset(self,_X0:"target logger",
                _X1:"message to log"):
    self._log_base(_X0,_X1,"dim","dim",_X4=print)
  def default(self,_X0,_X1):self.notset(_X0,_X1)
  def info(self,_X0:"target logger",
                _X1:"message to log"):
    self._log_base(_X0,_X1,"normal","blue")
  def information(self,_X0,_X1):self.info(_X0,_X1)
  def debug(self,_X0:"target logger",
                 _X1:"message to log"):
    self._log_base(_X0,_X1,"dim","purple")
  def trace(self,_X0:"target logger",
                 _X1:"message to log"):
    self._log_base(_X0,_X1,"dim","magenta")
  def warn(self,_X0:"target logger",
                _X1:"message to log"):
    self._log_base(_X0,_X1,"normal","bold orange_red1")
  def warning(self,_X0,_X1):self.warn(_X0,_X1)
  def error(self,_X0:"target logger",
                 _X1:"message to log"):
    self._log_base(_X0,_X1,"normal","bold red")
  def critical(self,_X0:"target logger",
                    _X1:"message to log"):
    self._log_base(_X0,_X1,"normal","bold reverse red")

class QExceptionHandler:
  def __init__(self):pass
  def install(self,_X0:"install target"):
    _X0.excepthook=self.excepthook
  def traceback(self,_X0:"traceback"):
    print()
    try:print(f"\r  | file: {_X0.tb_frame.f_code.co_filename}")
    except:pass
    try:print(f"\r  | line: {_X0.tb_lineno} ")
    except:pass
  def excepthook(self,_X0:"exception type",
                      _X1:"exception message",
                      _X2:"exception traceback"):
    if _X0 in(_T0:=sum(unwrap_b(__builtins__).items(),())):
      _T1:"exception id"=sys.getsizeof(_X0)+_T0.index(_X0)
    else:
      _T1=f"{id(_X0)}"[::-1][:6][::-1]
    _0:"exception logger id"=QLogId(_T1,_X0.__name__)
    _1:"exception logger"=QLog(log_level=QLevel.Warn,date=None)
    self.traceback(_X2)
    _1.warn(_0,_X1)
   
rich.pretty.install() 
if _QLOG_TRACEBACK=="rich":
 import rich.traceback
 rich.traceback.install()
else:
 qexc=QExceptionHandler()
 qexc.install(sys)