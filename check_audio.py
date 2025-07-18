import sounddevice as sd

print("Querying for audio devices...")
print(sd.query_devices())
print("Query finished.")
