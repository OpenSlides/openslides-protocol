(function () {

'use strict';

angular.module('OpenSlidesApp.openslides_protocol.site', ['OpenSlidesApp.openslides_protocol'])

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
            'collectionName': 'openslides_protocol/item-protocol',
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

.factory('ItemProtocolDialog', [
    'gettextCatalog',
    'Mediafile',
    'Editor',
    'ItemProtocol',
    function (gettextCatalog, Mediafile, Editor, ItemProtocol) {
        return {
            getDialog: function (item) {
                var protocol = _.find(ItemProtocol.getAll(), function (protocol) {
                    return protocol.item.id === item.id;
                });
                 return {
                    template: 'static/templates/openslides_protocol/item-protocol-form.html',
                    controller: protocol ? 'ProtocolEditCtrl' : 'ProtocolCreateCtrl',
                    className: 'ngdialog-theme-default wide-form',
                    closeByEscape: false,
                    closeByDocument: false,
                    resolve: {
                        item: function () {return item; },
                        protocol: function () {return protocol; },
                    },
                };
            },
            getFormFields: function () {
                var images = Mediafile.getAllImages();
                return [
                    {
                        key: 'protocol',
                        type: 'editor',
                        templateOptions: {
                            label: gettextCatalog.getString('Protocol'),
                        },
                        data: {
                            ckeditorOptions: Editor.getOptions(images)
                        }
                    },
                ];
            },
        };
    }
])

.controller('ProtocolListCtrl', [
    '$scope',
    'ItemProtocol',
    'Agenda',
    'AgendaTree',
    'Motion',
    'Assignment',
    'AssignmentPhases',
    'User',
    function ($scope, ItemProtocol, Agenda, AgendaTree, Motion, Assignment, AssignmentPhases, User) {
        $scope.$watch(function () {
            return Agenda.lastModified();
         }, function () {
            // Filter out items that doesn't have the list_item_title. This happens, if the
            // item is a hidden item but provides the list of speakers, but should not be
            // visible in the list view.
            var allowedItems = _.filter(Agenda.getAll(), function (item) {
                return item.list_view_title;
            });
            $scope.items = AgendaTree.getFlatTree(allowedItems);
        });
        ItemProtocol.bindAll({}, $scope, 'itemProtocols');
        Motion.bindAll({}, $scope, 'motions');
        Assignment.bindAll({}, $scope, 'assignments');
        User.bindAll({}, $scope, 'users');
        $scope.phases = AssignmentPhases;

        $scope.selectText = function () {
            var elementId = $scope.activeTab + 'SelectContainer';
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
        $scope.hasProtocol = function (item) {
            return _.some(ItemProtocol.getAll(), function (protocol) {
                return protocol.item.id === item.id;
            });
        };
        $scope.getProtocol = function (item) {
            return _.find(ItemProtocol.getAll(), function (protocol) {
                return protocol.item.id === item.id;
            });
        };
        $scope.itemProtocolSorter = function (itemProtocol) {
            return itemProtocol.item.weight;
        };
    }
])

.controller('ProtocolCreateCtrl', [
    '$scope',
    'ItemProtocol',
    'ItemProtocolDialog',
    'item',
    'ErrorMessage',
    function ($scope, ItemProtocol, ItemProtocolDialog, item, ErrorMessage) {
        $scope.model = {item_id: item.id};
        $scope.formFields = ItemProtocolDialog.getFormFields();

        $scope.save = function (model) {
            ItemProtocol.create(model).then(function (success) {
                $scope.closeThisDialog();
            }, function (error) {
                $scope.alert = ErrorMessage.forAlert(error);
            });
        };
    }
])

.controller('ProtocolEditCtrl', [
    '$scope',
    'ItemProtocol',
    'ItemProtocolDialog',
    'item',
    'protocol',
    'ErrorMessage',
    function ($scope, ItemProtocol, ItemProtocolDialog, item, protocol, ErrorMessage) {
        $scope.model = angular.copy(protocol);
        $scope.formFields = ItemProtocolDialog.getFormFields();
        $scope.deleteEnabled = true;

        $scope.save = function (model) {
            ItemProtocol.inject(model);
            ItemProtocol.save(model).then(function (success) {
                $scope.closeThisDialog();
            }, function (error) {
                ItemProtocol.refresh(model);
                $scope.alert = ErrorMessage.forAlert(error);
            });
        };
        $scope.delete = function (model) {
            ItemProtocol.destroy(model).then(function (success) {
                $scope.closeThisDialog();
            }, function (error) {
                $scope.alert = ErrorMessage.forAlert(error);
            });
        };
    }
])

.run([
    'templateHooks',
    'ngDialog',
    'ItemProtocolDialog',
    'ItemProtocol',
    function (templateHooks, ngDialog, ItemProtocolDialog, ItemProtocol) {
        templateHooks.registerHook({
            Id: 'agendaListAdditionalContentColumn',
            templateUrl: 'static/templates/openslides_protocol/agenda-hook.html',
            scope: {
                openProtocolDialog: function (item) {
                    console.log("test");
                    ngDialog.open(ItemProtocolDialog.getDialog(item));
                },
                hasProtocol: function (item) {
                    return _.some(ItemProtocol.getAll(), function (protocol) {
                        return protocol.item.id === item.id;
                    });
                },
                getPlainProtocolText: function (item) {
                    var protocol = _.find(ItemProtocol.getAll(), function (protocol) {
                        return protocol.item.id === item.id;
                    });
                    return protocol ? $(protocol.protocol).text() : '';
                },
            },
        });
    }
]);

}());
