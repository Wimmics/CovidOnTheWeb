db.spotlight_light.drop()
db.spotlight.aggregate([

    { $project: {
        'body_text': 0,
        'title.percentageOfSecondRank': 0,
        'title.support': 0,
        'abstract.percentageOfSecondRank': 0,
        'abstract.support': 0
        }
    },

    { $out: "spotlight_light" }
])

db.spotlight_light.createIndex({paper_id: 1})
