// Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

db.spotlight_light.drop()
db.spotlight.aggregate([

    // Remove the body and other un-needed fields
    { $project: {
        'body_text': 0,
        'title.percentageOfSecondRank': 0,
        'title.support': 0,
        'abstract.percentageOfSecondRank': 0,
        'abstract.support': 0
        }
    },

    // Keep only named entities:
    // (1) with a URI (should be all of them)
    // (2) with a similarityScore higher than 0.75
    // (3) that are at least 3 characters long
    { $project: {
        paper_id: 1,

        'title': { $filter: { input: "$title",  cond: { $and: [
            { $ne: ["$$this.URI", undefined] },
            { $gte: ["$$this.similarityScore", 0.75] },
            { $gte: [{$strLenCP: "$$this.surfaceForm"}, 3] }
        ]}}},
        
        'abstract': { $filter: { input: "$abstract",  cond: { $and: [
            { $ne: ["$$this.URI", undefined] },
            { $gte: ["$$this.similarityScore", 0.75] },
            { $gte: [{$strLenCP: "$$this.surfaceForm"}, 3] }
        ]}}}
    }},

    { $out: "spotlight_light" }
])

db.spotlight_light.createIndex({paper_id: 1})
