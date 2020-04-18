// Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

db.cord19_json_light.drop()
db.cord19_json.aggregate([

    // Keep only paper_id and authors
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
