# Changelog
All notable changes to this project will be documented in this file.

The format of this changelog is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [2.0.1]
### Added
- Test on Django 5.0 and 5.1.
- Test on Python 3.12 and 3.13 (for Django versions with support).
- Testing with Pypy 3.10 on Django < 4.1 (see note about Pypy in 'Removed' section).

### Removed
- Stop building a universal wheel.
- Remove testing with Pypy for Django >= 4.1. There is a Pypy bug preventing Django from working:
  https://code.djangoproject.com/ticket/33889

## [2.0.0]
### Changed
- Use Model.__str__() for related fields. In 1.x the primary key was used for related fields.

### Added
- Test on Django 3.2, 4.0, 4.1 and 4.2.
- Test on Python 3.9, 3.10 and 3.11 (for Django versions with support).
- Add `verbose_names` option to control whether to use capitalized verbose column names in the header. The default is
 `True` which matches the behaviour in 1.x.

### Removed
- Drop support for Python 2, 3.4 and 3.5.
- Drop support for Django 1.11, 2.0, 2.1, 3.0 and 3.1.
  - Django 3.1 was never supported in an official release, but it was tested in a pre-release version.

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

[2.0.1]: https://github.com/benkonrath/django-csv-export-view/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/benkonrath/django-csv-export-view/compare/1.1.0...2.0.0
[1.1.0]: https://github.com/benkonrath/django-csv-export-view/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/benkonrath/django-csv-export-view/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.5.0...1.0.0
[0.5.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/benkonrath/django-csv-export-view/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/benkonrath/django-csv-export-view/compare/4a8792dbaf97c7fdb5de77dbc9fc0c28c5c54eab...0.1.0
