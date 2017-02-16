'use strict';

const request = require('request');
const expect = require('chai').expect;
const optimist = require('optimist');

function __getApiKey__() {
    return "skynetSuperSecretApiKey";
}

const lineCommands = optimist.argv;
const skynetApiUrl = lineCommands.docker ? 'http://dev.l0cal/' : 'http://localhost:8080/';


describe('API', () => {
    describe('autoBuy full lifecycle', () => {
        it('load should return no error', (done) => { load(done, false); });
        it('start should return no error', (done) => { start(done, false); });
        it('stop should return no error', (done) => { stop(done, false); });
        it('unload should return no error', (done) => { unload(done, false); });
    });

    describe('autoBuy half lifecycle', () => {
        it('load should return no error', (done) => { load(done, false); });
        it('unload should return no error', (done) => { unload(done, false); });
    });

    describe('autoBuy test after unload', () => {
        it('load should return no error', (done) => { load(done, false); });
        it('start should return no error', (done) => { start(done, false); });
        it('unload should return no error', (done) => { unload(done, false); });
        it('start should fail', (done) => { start(done, true); });
        it('stop should fail', (done) => { stop(done, true); });
        it('load should return no error', (done) => { load(done, false); });
    });

    describe('autoBuy test not loaded', () => {
        it('unload should return no error', (done) => { unload(done, false); });
        it('start should fail', (done) => { start(done, true); });
        it('stop should fail', (done) => { stop(done, true); });
        it('unload should fail', (done) => { unload(done, true); });
    });

    describe('autoBuy test not started and check for double actions', () => {
        it('load should return no error', (done) => { load(done, false); });
        it('stop should fail', (done) => { stop(done, true); });
        it('start should return no error', (done) => { start(done, false); });
        it('start should fail', (done) => { start(done, true); });
        it('stop should return no error', (done) => { stop(done, false); });
        it('stop should fail', (done) => { stop(done, true); });
        it('unload should return no error', (done) => { unload(done, false); });
        it('unload should fail', (done) => { unload(done, true); });
    });
});

let load = (done, errorExpected) => {
    _postToAutoBuy(done, errorExpected, 'load');
};

let unload = (done, errorExpected) => {
    _postToAutoBuy(done, errorExpected, 'unload');
};

let start = (done, errorExpected) => {
    _postToAutoBuy(done, errorExpected, 'start');
};

let stop = (done, errorExpected) => {
    _postToAutoBuy(done, errorExpected, 'stop');
};

let _postToAutoBuy = (done, errorExpected, route) => {
    request.post({
        'url': `${skynetApiUrl}network/autoBuy/${route}`,
        'body': '{"skynetApiKey": "' + __getApiKey__() + '"}'
    }, (err, httpResponse, body) => {
        body = JSON.parse(body);
        expect(err).to.equal(null);
        expect(httpResponse.statusCode).to.equal(200);
        errorExpected ? expect(body.error).to.not.equal(null) : expect(body.error).to.equal(null);
        done();
    });
};
