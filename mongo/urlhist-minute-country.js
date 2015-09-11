var cursor = db.urlhist.aggregate([
    {$project: {
        day: {$dayOfMonth: "$timestamp"},
        hour: {$hour: "$timestamp"},
        minute: {$minute: "$timestamp"},
        country: "$country",
        _id: 0
    }},
    /* Group by day, hour, minute, and country */
    {$group: {
        _id: {day: "$day", hour: "$hour", minute: "$minute", country: "$country"},
        count: {$sum: 1}
    }},
    /* Limit to more then 100 hits per minute interval */
    /*{$match: {
        count: {$gte: 100}
    }},*/
    /* Sort works in an unexpected way */
    {$sort: {
        day: 1,
        hour: 1,
        minute: 1,
        count: -1,
        country: 1
    }}
]);

/*
function printResult(r) {
    print(tojson(r));
}
*/

function convert(r) {
    return {day: r._id.day, hour: r._id.hour, minute: r._id.minute, country: r._id.country, count: r.count};
}
function write(doc) {
    print(tojson(doc));
}
/* cursor.forEach(printResult);*/

cursor.forEach(convert).forEach(write);
