# Changelog
All notable changes to this project will be documented in this file.

The format of this changelog is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Use Model.__str__() for related fields. In 1.x the primary key was used for related fields.

### Added
- Test on Django 3.0, 3.1 & 3.2
- Test on Python 3.9 (for Django versions with support).

### Removed
- Drop support for Python 2 and Python 3.4.
- Drop support for Django 1.11.

## [1.1.0]
### Added
- Add support for Django 3.0.
- Test on Python 3.8 (for Django versions with support).

## [1.0.1]
### Added
- Test on Django 2.2.

### Fixed
- Fixed bug with filename getting duplicate .csv extension.

## [1.0.0]
### Added
- Add CHANGELOG.md to release.

## [0.5.0]
### Added
- Test on Django 2.0 and 2.1.
- Test with pypy and pypy3.5.

### Removed
- Drop testing on Django < 1.11.

## [0.4.0]
### Fixed
- Fixed bug with numeric choice fields with 0 values.

## [0.3.0]
### Added
- More documentation in the README.
- More tests.
- Check that `get_context_data(self, **kwargs)` is not being overridden.

### Fixed
- Fixed issue with unicode csv data on Python 2.

### Removed
- Drop support for Python 3.3.

## [0.2.0] - 2017-08-07
### Added
- Allow `get_fields(self, queryset)` to be overridden.

### Fixed
- Fixed issue with blank value in choice field.

## [0.1.0] - 2017-08-01
### Added
- Initial version.

[Unreleased]: https://github.com/benkonrath/django-csv-export-view/compare/1.1.0...HEAD
[1.1.0]: https://github.com/benkonrath/django-csv-export-view/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/benkonrath/django-csv-export-view/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.5.0...1.0.0
[0.5.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/benkonrath/django-csv-export-view/compare/4a8792dbaf97c7fdb5de77dbc9fc0c28c5c54eab...0.1.0
