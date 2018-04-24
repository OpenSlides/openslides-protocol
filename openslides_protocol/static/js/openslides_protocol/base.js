(function () {

'use strict';

angular.module('OpenSlidesApp.openslides_protocol', [
    'OpenSlidesApp.core.site',
    'OpenSlidesApp.openslides_protocol',
    'OpenSlidesApp.openslides_protocol.templates',
])

.config([
    'OpenSlidesPluginsProvider',
    function(OpenSlidesPluginsProvider) {
        OpenSlidesPluginsProvider.registerPlugin({
            name: 'openslides_protocol',
            display_name: 'Protocol',
            languages: ['de']
        });
    }
])

.factory('ObjectProtocol', [
    'DS',
    'gettext',
    'operator',
    'CamelCase',
    'EditForm',
    function (DS, gettext, operator, CamelCase, EditForm) {
        var name = 'openslides_protocol/object-protocol';
        return DS.defineResource({
            name: name,
            methods: {
                getResourceName: function () {
                    return name;
                },
                getContentObject: function () {
                    return DS.get(this.content_object.collection, this.content_object.id);
                },
                getContentObjectDetailState: function () {
                    return CamelCase(this.content_object.collection).replace('/', '.') +
                        '.detail({id: ' + this.content_object.id + '})';
                },
                getContentObjectForm: function () {
                    return EditForm.fromCollectionString(this.content_object.collection);
                },
                getContentResource: function () {
                    return DS.definitions[this.content_object.collection];
                },
            },
        });
    }
])

.factory('Protocol', [
    'DS',
    'gettext',
    'operator',
    'ObjectProtocol',
    function (DS, gettext, operator, ObjectProtocol) {
        var getNextIdForText = function (protocol) {
            var highestIdFound = -1;
            _.forEach(protocol, function (entry) {
                if (entry.type === 'text' && entry.id > highestIdFound) {
                    highestIdFound = entry.id;
                }
            });
            return highestIdFound+1;
        };

        var name = 'openslides_protocol/protocol';
        return DS.defineResource({
            name: name,
            methods: {
                add: function (obj, type) {
                    if (!type) {
                        type = obj.getResourceName();
                    }
                    
                    var entry = {
                        type: type,
                        id: obj.id || undefined,
                    };
                    if (type === 'text') {
                        entry.title = obj.title;
                        entry.text = obj.text;
                        entry.id = getNextIdForText(this.protocol);
                    }
                    if (typeof entry.id === 'undefined') {
                        throw "The object has to have an id (except type 'text').";
                    }
                    if (entry.id) {
                        _.forEach(this.protocol, function(protocolEntry) {
                            if (entry.id === protocolEntry.id && entry.type === protocolEntry.type) {
                                throw "This entry (" + entry.type + ", id: " + entry.id +
                                    ") is already in the protocol.";
                            }
                        });
                    }
                    this.protocol.push(entry);
                    DS.save(name, this.id);
                },
                remove: function (obj) {
                    if ((typeof obj.id === 'undefined') || !obj.type) {
                        throw "An id and type have to be given!";
                    }
                    this.protocol = _.filter(this.protocol, function (entry) {
                        return (obj.id !== entry.id || obj.type !== entry.type);
                    });
                    DS.save(name, this.id);
                },
                used: function (obj) {
                    var resourceName = obj.getResourceName();
                    return _.some(this.protocol, function (entry) {
                        return (obj.id === entry.id && resourceName === entry.type);
                    });
                },
            },
        });
    }
])

.run(['ObjectProtocol', 'Protocol', function (ObjectProtocol, Protocol) {}]);

}());
