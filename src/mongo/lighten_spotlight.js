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

    { $project: {
        paper_id: 1,

        'title': { $filter: { input: "$title",  cond: { $and: [
            // Keep only entites with a URI (should be all of them)
            { $ne: ["$$this.URI", undefined] },

            // Keep only entites with a similarityScore higher than 0.75
            { $gte: ["$$this.similarityScore", 0.75] },
            
            // Keep only named entites that are at least 3 characters long
            { $gte: [{$strLenCP: "$$this.surfaceForm"}, 3] }
        ]}}},
        
        'abstract': { $filter: { input: "$abstract",  cond: { $and: [
            // Keep only entites with a URI (should be all of them)
            { $ne: ["$$this.URI", undefined] },

            // Keep only entites with a similarityScore higher than 0.75
            { $gte: ["$$this.similarityScore", 0.75] },
            
            // Keep only named entites that are at least 4 characters long
            { $gte: [{$strLenCP: "$$this.surfaceForm"}, 4] }
        ]}}}
    }},

    { $out: "spotlight_light" }
])

db.spotlight_light.createIndex({paper_id: 1})
