db.entityfishing_light.drop()
db.entityfishing.aggregate([

    // Keep only entities with a wikidataId field
    { $project: {
        'paper_id': 1,

        'title.entities': {$filter: { input: "$title.entities", cond: { $ne: [ "$$this.wikidataId", undefined ] }}},
        'title.global_categories': 1,

        'abstract.entities': { $filter: { input: "$abstract.entities", cond: { $ne: [ "$$this.wikidataId", undefined ] }}},
        'abstract.global_categories': 1,

        'body_text.entities': { $filter: { input: "$body_text.entities", cond: { $ne: [ "$$this.wikidataId", undefined ] }}},
        'body_text.global_categories': 1
    }},

    // Remove un-needed fields
    { $project: {
        'title.global_categories.weight': 0,
        'title.global_categories.source': 0,
        'title.entities.nerd_selection_score': 0,
        'title.entities.wikipediaExternalRef': 0,

        'abstract.global_categories.weight': 0,
        'abstract.global_categories.source': 0,
        'abstract.entities.nerd_selection_score': 0,
        'abstract.entities.wikipediaExternalRef': 0,

        'body_text.global_categories.weight': 0,
        'body_text.global_categories.source': 0,
        'body_text.entities.nerd_selection_score': 0,
        'body_text.entities.wikipediaExternalRef': 0
        }
    },

    { $out: "entityfishing_light" }
])

db.entityfishing_light.createIndex({paper_id: 1})
