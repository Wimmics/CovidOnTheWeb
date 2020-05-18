// Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


// ------------------------------------------------ Filter only support relations
db.acta_support.drop()
db.acta.aggregate([

    // Keep only support relations
    { $project: {
        'paper_id': 1,
        'relations': { $filter: { input: "$relations",  cond: { $eq: ["$$this.type", "support"] }}},
    }},

    // Keep only non-empty relations
    { $addFields: { 'relations_length': {$size: "$relations"}}},
    { $match: {'relations_length': { $gt: 0 }}},
    { $project: { components_length: 0}},

    { $out: "acta_support" }
])
db.acta_support.createIndex({paper_id: 1})


// ------------------------------------------------ Filter only attack relations
db.acta_attack.drop()
db.acta.aggregate([

    // Keep only attack relations
    { $project: {
        'paper_id': 1,
        'relations': { $filter: { input: "$relations",  cond: { $eq: ["$$this.type", "attack"] }}},
    }},

    // Keep only non-empty relations
    { $addFields: { 'relations_length': {$size: "$relations"}}},
    { $match: {'relations_length': { $gt: 0 }}},
    { $project: { components_length: 0}},

    { $out: "acta_attack" }
])
db.acta_attack.createIndex({paper_id: 1})


// ------------------------------------------------ Unwind components
db.acta_components.drop()
db.acta.aggregate([

    // Keep only non-empty components
    { $addFields: { 'components_length': { $size: "$components" }}},
    { $match: { components_length: { $gt: 0 }}},
    { $project: { _id: 0, components_length: 0, relations: 0 }},
    
    // Unwind components (create one doc per component)
    { $unwind: "$components" },
    { $addFields: { id: "$components.id" }},
    { $addFields: { text: "$components.text" }},
    { $addFields: { type: "$components.type" }},
    { $addFields: { outcome: "$components.outcome" }},
    { $addFields: { intervention: "$components.intervention" }},
    { $addFields: { participants: "$components.participants" }},
    { $project: { components: 0 }},
    
    { $out: "acta_components" }
])
db.acta_components.createIndex({paper_id: 1})


// ------------------------------------------------ Unwind PICO elements

db.acta_components_outcomes.drop()
db.acta_components.aggregate([
    // Keep only non-empty outcomes
    { $match: { "outcome": { $ne: null }}},
    { $addFields: { 'outcome_length': { $size: "$outcome" }}},
    { $match: { outcome_length: { $gt: 0 }}},
    { $project: { _id: 0, outcome_length: 0, participants: 0, intervention: 0 }},
    
    // Unwind outcomes
    { $unwind: "$outcome" },
    { $match: { "outcome.linked_to": { $ne: null }}},
    { $addFields: { pico_text: "$outcome.text" }},
    { $addFields: { linked_to: "$outcome.linked_to" }},
    { $project: { outcome: 0 }},
    
    { $out: "acta_components_outcomes" }
])
db.acta_components_outcomes.createIndex({paper_id: 1})


db.acta_components_intervention.drop()
db.acta_components.aggregate([
    // Keep only non-empty intervention
    { $match: { "intervention": { $ne: null }}},
    { $addFields: { 'intervention_length': { $size: "$intervention" }}},
    { $match: { intervention_length: { $gt: 0 }}},
    { $project: { _id: 0, intervention_length: 0, participants: 0, outcome: 0 }},
    
    // Unwind intervention
    { $unwind: "$intervention" },
    { $match: { "intervention.linked_to": { $ne: null }}},
    { $addFields: { pico_text: "$intervention.text" }},
    { $addFields: { linked_to: "$intervention.linked_to" }},
    { $project: { intervention: 0 }},
    
    { $out: "acta_components_intervention" }
])
db.acta_components_intervention.createIndex({paper_id: 1})


db.acta_components_participants.drop()
db.acta_components.aggregate([
    // Keep only non-empty participants
    { $match: { "participants": { $ne: null }}},
    { $addFields: { 'participants_length': { $size: "$participants" }}},
    { $match: { participants_length: { $gt: 0 }}},
    { $project: { _id: 0, participants_length: 0, intervention: 0, outcome: 0 }},
    
    // Unwind participants
    { $unwind: "$participants" },
    { $match: { "participants.linked_to": { $ne: null }}},
    { $addFields: { pico_text: "$participants.text" }},
    { $addFields: { linked_to: "$participants.linked_to" }},
    { $project: { participants: 0 }},
    
    { $out: "acta_components_participants" }
])
db.acta_components_participants.createIndex({paper_id: 1})
