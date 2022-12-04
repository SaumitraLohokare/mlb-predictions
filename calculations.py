from pymongo.collection import Collection

def calculate(coll: Collection):
    result = {}
    entries = coll.find({})
    for entry in entries:
        rpb = entry["R"] / (entry["H"] + entry["BB"])
        # Uncomment to update in db
        # coll.update_one(
        #     { "_id": entry["_id"] },
        #     { "RPB": rpb}
        # )
        result[entry["Tm"]] = rpb
    return result