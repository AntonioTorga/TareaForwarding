import router as rt

txt = "127.0.0.1,8881,4,hola"
txt_p = rt.parse_packet(txt.encode())
print(txt)
print(txt_p)
txt_dp = rt.create_packet({"IP":txt_p["IP"],"PORT":txt_p["PORT"],"TTL":txt_p["TTL"],"MSG":txt_p["MSG"]})
print(txt_dp.decode()==txt)