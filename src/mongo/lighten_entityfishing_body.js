// Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

db.COLLECTION_body.drop()
db.COLLECTION.aggregate([

    // Remove the body and other un-needed fields
    { $project: {
        'title': 0,
        'abstract': 0,
        
        'body_text.global_categories.weight': 0,
        'body_text.global_categories.source': 0,
        'body_text.entities.nerd_selection_score': 0,
        'body_text.entities.wikipediaExternalRef': 0
        }
    },

    { $project: {
        'paper_id': 1,

        // Keep only named entities that (1) are at least 3 characters long and (2) have a wikidataId field
        'body_text.entities': { $filter: { input: "$body_text.entities",  cond: { $and: [
            { $ne:  ["$$this.wikidataId", undefined] },
            { $gte: [{$strLenCP: "$$this.rawName"}, 3] }
        ]}}},
        'body_text.global_categories': 1
    }},

    { $out: "COLLECTION_body" }
])

db.COLLECTION_body.createIndex({paper_id: 1})
