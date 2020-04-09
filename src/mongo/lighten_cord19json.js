db.cord19_json_light.drop()
db.cord19_json.aggregate([

    { $project: {
        paper_id: 1,
        metadata: 1
    }},

    { $out: "cord19_json_light" }
])

db.cord19_json_light.createIndex({paper_id: 1})
