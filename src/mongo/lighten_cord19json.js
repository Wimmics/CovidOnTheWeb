db.cord19_json_light.drop()
db.cord19_json.aggregate([

    { $project: {
        paper_id: 1,
        
        // Filter out authors whose first or last name starts with a non-alphabetical character (issues with names starting with '(' or '-'
        'metadata.authors': { $filter: { input: "$metadata.authors",  cond: {
            $regexMatch: { input: "$$this.last", regex: /^[a-zA-Z]/ }
        }}}
    }},

    { $out: "cord19_json_light" }
])

db.cord19_json_light.createIndex({paper_id: 1})
