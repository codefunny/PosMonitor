import pyDes
import binascii as ba

k1 = "1073E6190825D37029C4A838EA80C43B"
pinkey = "1234567890abcdef1234567890abcdef"
#982af773a7ab8576d651190ea4b6abf7,b9808685dae55d0d
mackey = "abcdef0123456789"
k = pyDes.triple_des(ba.a2b_hex(k1))
pinkey = k.encrypt(ba.a2b_hex(pinkey))
mackey = k.encrypt(ba.a2b_hex(mackey))
pinkey = ba.b2a_hex(pinkey)
mackey = ba.b2a_hex(mackey)
#mackey = mackey.ljust(32,'0')
print("%s,%s"%(pinkey,mackey))
h62 = pinkey+"00000000"
l62 = mackey+"00000000"


pinkey = k.decrypt(ba.a2b_hex(pinkey))
mackey = k.decrypt(ba.a2b_hex(mackey))
pinkey = ba.b2a_hex(pinkey)
mackey = ba.b2a_hex(mackey)

print pinkey,mackey
