(function () {

'use strict';

angular.module('OpenSlidesApp.openslides_protocol.site', [
    'OpenSlidesApp.openslides_protocol',
    'OpenSlidesApp.openslides_protocol.templatehooks',
])

.config([
    'mainMenuProvider',
    'gettext',
    function (mainMenuProvider, gettext) {
        mainMenuProvider.register({
            'ui_sref': 'openslides_protocol.protocol.list',
            'img_class': 'pencil',
            'title': gettext('Protocol'),
            'weight': 700,
            'perm': 'openslides_protocol.can_write_protocol',
        });
    }
])

.config([
    'SearchProvider',
    'gettext',
    function (SearchProvider, gettext) {
        SearchProvider.register({
            'verboseName': gettext('Protocol'),
            'collectionName': 'openslides_protocol/object-protocol',
            'urlDetailState': 'motions.motion.detail',
            'weight': 300,
        });
    }
])

.config([
    '$stateProvider',
    function ($stateProvider) {
        $stateProvider
        .state('openslides_protocol', {
            url: '/protocol',
            abstract: true,
            template: "<ui-view/>",
        })
        .state('openslides_protocol.protocol', {
            abstract: true,
            template: "<ui-view/>",
        })
        .state('openslides_protocol.protocol.list', {
        });
    }
])

.factory('ObjectProtocolDialog', [
    'gettextCatalog',
    'Editor',
    'ObjectProtocol',
    function (gettextCatalog, Editor, ObjectProtocol) {
        return {
            getDialog: function (contentObject, deleteEnabled) {
                var objectProtocol = _.find(ObjectProtocol.getAll(), function (protocol) {
                    return protocol.content_object.collection === contentObject.getResourceName() &&
                        protocol.content_object.id === contentObject.id;
                });
                return {
                    template: 'static/templates/openslides_protocol/object-protocol-form.html',
                    controller: !!objectProtocol ? 'ObjectProtocolEditCtrl' : 'ObjectProtocolCreateCtrl',
                    className: 'ngdialog-theme-default wide-form',
                    closeByEscape: false,
                    closeByDocument: false,
                    resolve: {
                        contentObject: function () { return contentObject; },
                        objectProtocol: function () { return objectProtocol; },
                        deleteEnabled: function () { return deleteEnabled && !!objectProtocol; },
                    },
                };
            },
            getFormFields: function () {
                return [
                    {
                        key: 'protocol',
                        type: 'editor',
                        templateOptions: {
                            label: gettextCatalog.getString('Protocol'),
                        },
                        data: {
                            ckeditorOptions: Editor.getOptions(),
                        }
                    },
                ];
            },
        };
    }
])

.factory('FreeTextDialog', [
    'gettextCatalog',
    'Editor',
    function (gettextCatalog, Editor) {
        return {
            getDialog: function (entry, protocol) {
                 return {
                    template: 'static/templates/openslides_protocol/object-protocol-form.html',
                    controller: 'FreeTextEditCtrl',
                    className: 'ngdialog-theme-default wide-form',
                    closeByEscape: false,
                    closeByDocument: false,
                    resolve: {
                        entry: function () {return entry; },
                        protocol: function () {return protocol; },
                    },
                };
            },
            getFormFields: function () {
                return [
                    {
                        key: 'title',
                        type: 'input',
                        templateOptions: {
                            label: gettextCatalog.getString('Title'),
                        },
                    },
                    {
                        key: 'text',
                        type: 'editor',
                        templateOptions: {
                            label: gettextCatalog.getString('Text'),
                        },
                        data: {
                            ckeditorOptions: Editor.getOptions()
                        }
                    },
                ];
            },
        };
    }
])

.controller('ProtocolListCtrl', [
    '$scope',
    '$filter',
    'gettextCatalog',
    'DS',
    'ObjectProtocol',
    'Agenda',
    'AgendaTree',
    'Motion',
    'Assignment',
    'AssignmentPhases',
    'Protocol',
    'ngDialog',
    'ObjectProtocolDialog',
    'FreeTextDialog',
    function ($scope, $filter, gettextCatalog, DS, ObjectProtocol, Agenda, AgendaTree,
        Motion, Assignment, AssignmentPhases, Protocol, ngDialog,
        ObjectProtocolDialog, FreeTextDialog) {
        $scope.$watch(function () {
            return Agenda.lastModified();
        }, function () {
            $scope.items = _.map(AgendaTree.getFlatTree(Agenda.getAll()), function (item) {
                return item.getContentObject();
            });
        });
        ObjectProtocol.bindAll({}, $scope, 'objectProtocols');
        Motion.bindAll({}, $scope, 'motions');
        Assignment.bindAll({}, $scope, 'assignments');
        $scope.phases = AssignmentPhases;

        $scope.$watch(function () {
            return Protocol.lastModified();
        }, function () {
            $scope.protocol = Protocol.get(1);
        });

        $scope.addFreeText = function () {
            $scope.protocol.add({
                title: gettextCatalog.getString('Free text'),
                text: gettextCatalog.getString('New free text'),
            }, 'text');
        };
        $scope.treeOptions = {
            dropped: function (event) {
                Protocol.save($scope.protocol);
            },
        };
        $scope.edit = function (entry) {
            if (entry.type === 'text') {
                ngDialog.open(FreeTextDialog.getDialog(entry, $scope.protocol));
            } else {
                ngDialog.open(ObjectProtocolDialog.getDialog($scope.getObject(entry)));
            }
        };

        // Searching
        $scope.getItemProtocolQueryString = function (item) {
            return [$scope.getProtocol(item.id), item.getListViewTitle()].join(' ');
        };
        $scope.getMotionQueryString = function (motion) {
            return [
                motion.getTitle(),
                motion.getText(),
                motion.identifier,
                _.map(motion.submitters, function (submitter) {
                    return submitter.get_short_name();
                }).join(' '),
                _.map(motion.tags, function (tag) {
                    return tag.name;
                }).join(' '),
                motion.category ? motion.category.name : '',
                motion.origin
            ].join(' ');
        };
        $scope.getAssignmentQueryString = function (assignment) {
            return [
                assignment.title,
                _.map(assignment.assignment_related_users, function (candidate) {
                    return candidate.get_short_name();
                }).join(' '),
                _.map(assignment.tags, function (tag) {
                    return tag.name;
                }).join(' '),
                gettextCatalog.getString($scope.phases[assignment.phase].display_name)
            ].join(' ');
        };

        // Preview
        $scope.getObject = function (obj) {
            return DS.get(obj.type, obj.id);
        };
        $scope.hasProtocol = function (obj) {
            return _.some(ObjectProtocol.getAll(), function (protocol) {
                    return protocol.content_object.collection === obj.type &&
                        protocol.content_object.id === obj.id;
            });
        };
        $scope.getProtocol = function (obj) {
            return _.find(ObjectProtocol.getAll(), function (protocol) {
                    return protocol.content_object.collection === obj.type &&
                        protocol.content_object.id === obj.id;
            }).protocol;
        };
        $scope.getTypeVerboseName = function (obj) {
            return DS.definitions[$scope.getObject(obj).getResourceName()].verboseName;
        };

        $scope.selectProtocol = function () {
            var elementId = 'selectContainer';
            var element = document.getElementById(elementId);
            var range;
            if (document.body.createTextRange) {
                range = document.body.createTextRange();
                range.moveToElementText(element);
                range.select();
            } else if (window.getSelection) {
                var selection = window.getSelection();        
                range = document.createRange();
                range.selectNodeContents(element);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        };
    }
])

.controller('ObjectProtocolCreateCtrl', [
    '$scope',
    'gettextCatalog',
    'ObjectProtocol',
    'ObjectProtocolDialog',
    'contentObject',
    'deleteEnabled',
    'ErrorMessage',
    'DS',
    function ($scope, gettextCatalog, ObjectProtocol, ObjectProtocolDialog, contentObject, deleteEnabled, ErrorMessage, DS) {
        $scope.model = {
            content_object: {
                collection: contentObject.getResourceName(),
                id: contentObject.id,
            },
        };
        $scope.objectVerboseName = contentObject.agenda_item.getTitle();
        $scope.formFields = ObjectProtocolDialog.getFormFields();
        $scope.deleteEnabled = deleteEnabled;

        $scope.save = function (model) {
            ObjectProtocol.create(model).then(function (success) {
                $scope.closeThisDialog();
            }, function (error) {
                $scope.alert = ErrorMessage.forAlert(error);
            });
        };
    }
])

.controller('ObjectProtocolEditCtrl', [
    '$scope',
    'gettextCatalog',
    'ObjectProtocol',
    'ObjectProtocolDialog',
    'contentObject',
    'objectProtocol',
    'deleteEnabled',
    'ErrorMessage',
    'DS',
    function ($scope, gettextCatalog, ObjectProtocol, ObjectProtocolDialog, contentObject,
        objectProtocol, deleteEnabled, ErrorMessage, DS) {
        $scope.model = angular.copy(objectProtocol);
        $scope.objectVerboseName = contentObject.agenda_item.getTitle();
        $scope.formFields = ObjectProtocolDialog.getFormFields();
        $scope.deleteEnabled = deleteEnabled;

        $scope.save = function (model) {
            ObjectProtocol.inject(model);
            ObjectProtocol.save(model).then(function (success) {
                $scope.closeThisDialog();
            }, function (error) {
                ObjectProtocol.refresh(model);
                $scope.alert = ErrorMessage.forAlert(error);
            });
        };
        $scope.delete = function (model) {
            ObjectProtocol.destroy(model).then(function (success) {
                $scope.closeThisDialog();
            }, function (error) {
                $scope.alert = ErrorMessage.forAlert(error);
            });
        };
    }
])

.controller('FreeTextEditCtrl', [
    '$scope',
    'FreeTextDialog',
    'Protocol',
    'protocol',
    'entry',
    'ErrorMessage',
    function ($scope, FreeTextDialog, Protocol, protocol, entry, ErrorMessage) {
        $scope.model = angular.copy(entry);
        $scope.formFields = FreeTextDialog.getFormFields();
        $scope.freetext = true;

        $scope.save = function (model) {
            var index = _.findIndex(protocol.protocol, function (protocolEntry) {
                return model.id === protocolEntry.id && model.type === protocolEntry.type;
            });
            protocol.protocol[index] = model;

            Protocol.inject(protocol);
            Protocol.save(protocol).then(function (success) {
                $scope.closeThisDialog();
            }, function (error) {
                Protocol.refresh(protocol);
                $scope.alert = ErrorMessage.forAlert(error);
            });
        };
    }
])

.filter('notUsed', [
    function () {
        return function (objs, protocol) {
            if (protocol) {
                return _.filter(objs, function (obj) {
                    return !protocol.used(obj);
                });
            }
        };
    }
])

.filter('plaintextLimit', [
    function () {
        return function (text, limit) {
            text = '<p>' + text + '</p>';
            text = $(text).text().replace('\n', '');
            if (text.length > limit) {
                text = text.substring(0, limit) + '...';
            }
            return text;
        };
    }
])

.config([
    'gettext',
    function (gettext) {
        // Permissions
        gettext('Can write protocol');
        // Config strings
        gettext('Add motion reason in protocol');
    }
]);

}());
