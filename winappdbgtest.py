# sample script to demonstrate use of winappdbg
# written by corelanc0d3r
# www.corelan.be // www.corelan-training.com // www.corelan-consulting.com
from winappdbg import *
from time import time, sleep
import sys
import string
import os
import subprocess


class Dbg:
	def __init__(self, app, delay=7):
		self.app = app
		self.delay = delay
		self.current_file = ''
		
	def event_handler(self, event):
		code = event.get_event_code()
			
		if code == win32.EXCEPTION_DEBUG_EVENT and event.is_last_chance():
			print("********************* Crash detected!!! ************************")
			# Get the thread which generated the event
			thread = Thread(event.get_tid())			
			# Get basic infomation about the event
			msg = str(Crash(event))

			# Try to disassembly the code around the fault instruction
			try:
				eip  = thread.get_pc()
				code = thread.disassemble_around(eip)
				msg += str(CrashDump.dump_code(code, eip))
			except WindowsError, e:
				pass
			
			# Log information about the crash (registers, disassemby, so on)
			#logger = Logger('crashes/' + filename + '.log')
			#logger.log_event(event, msg)
			
			# Attempt to kill the process
			event.get_process().kill()


	def run(self):
		testcase = 1
		while True:
			with Debug(self.event_handler, bKillOnExit=True) as dbg:
				
				System.set_kill_on_exit_mode(True)
				
				# get next case file... 
				# for the sake of the exercise, we'll use the same file every time
				self.current_file = 'c:\\test.txt'

				print("Case #%d: running %s %s" % (testcase, self.app, self.current_file))				
				dbg.execv([self.app] + [self.current_file])

				max_time = time() + self.delay
				while dbg and time() < max_time:
					try:
						# Get the next debug event.
						dbg.wait(1000)  # 1 second accuracy

					# If wait() times out just try again. On any other error stop debugging.
					except WindowsError, e:
						if e.winerror in (win32.ERROR_SEM_TIMEOUT, win32.WAIT_TIMEOUT):
							continue
						raise

					# Dispatch the event and continue execution.
					try:
						dbg.dispatch()
					finally:
						dbg.cont()
				
			testcase += 1
			

			# Kill any existing process of our target
			for (process, name) in dbg.system.find_processes_by_filename('notepad.exe'):
					#print process.get_pid(), name
					pid = process.get_pid()
					dbg.detach(process.get_pid())
					with open(os.devnull, "w") as fnull:
						subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)], stdout = fnull, stderr = fnull)


dbgengine = Dbg(r'c:\windows\system32\notepad.exe')
dbgengine.run()