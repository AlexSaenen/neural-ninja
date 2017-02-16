'use strict';

const fs = require('fs');
const request = require('request');
const expect = require('chai').expect;
const optimist = require('optimist');

function __getApiKey__() {
    return "skynetSuperSecretApiKey";
}

const lineCommands = optimist.argv;
const skynetApiUrl = lineCommands.docker ? 'http://dev.l0cal/' : 'http://localhost:8080/';

describe('uploadNetwork', () => {
    it('should successfully upload studentHours', (done) => {
        const reqBuilder = request.post({
            'url': `${skynetApiUrl}networks/upload`
        }, (err, httpResponse, body) => {
            body = JSON.parse(body);
            expect(err).to.equal(null);
            expect(httpResponse.statusCode).to.equal(200);
            expect(body.error).to.equal(null);
            expect(body.answer).to.equal("Network uploaded successfully");
            done();
        });

        const form = reqBuilder.form()
        form.append('skynetApiKey', __getApiKey__())
        console.log(__dirname);
        form.append('networkFile', fs.createReadStream(__dirname + '/../models/studentHours.py'))
    });
});
