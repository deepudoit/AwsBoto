exports.lambda_handler = function(event, context, callback) {
    callback(null, 'some success');
    return {
        "statusCode": 200,
        "message": "This is nodejs lambda"
    }
}