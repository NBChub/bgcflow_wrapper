# History
## 0.4.0 (2024-06-20)
- Upgrade Snakemake to v8.14.0
- **Fix**: Improve `get-result` command to be more intuitive
- **Docs**: Update citation
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.3.5...v0.4.0)

## 0.3.5 (2024-06-01)
- Snakemake fix and security update by @matinnuhamunada in https://github.com/NBChub/bgcflow_wrapper/pull/39
- **Fix**: Pin pulp version to 2.7.0 to address snakemake dependency issue: https://github.com/snakemake/snakemake/issues/2606
- **Feat**: add `--profile` parameters on `bgcflow` run to use snakemake profiles
- **Chore(deps)**: bump pip from 22.3.1 to 23.3 by @dependabot in https://github.com/NBChub/bgcflow_wrapper/pull/40
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.3.4...v0.3.5)

## 0.3.4 (2023-11-22)
- Synchronize with BGCFlow version 0.7.9
- **Feat**: add CLI option for lsabgc and ppanggolin by @matinnuhamunada in [PR #37](https://github.com/NBChub/bgcflow_wrapper/pull/37)
- **Chore**: Auto detect available CPU
- **Feat**: give option to turn off panoptes
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.3.3...v0.3.4)

## 0.3.3 (2023-11-20)
- **Fix**: Pin snakemake to v7.31.1 for compatibility with panoptes-ui job monitoring. [PR #35](https://github.com/NBChub/bgcflow_wrapper/pull/35)
- **Chore**: Security updates. [PR #35](https://github.com/NBChub/bgcflow_wrapper/pull/35)
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.3.2...v0.3.3)

## 0.3.2 (2023-10-12)
- Release package in [PyPi](https://pypi.org/project/bgcflow_wrapper)
- **Change**: Downgrade pandas. [PR #29](https://github.com/NBChub/bgcflow_wrapper/pull/29)
- **Chore**: Dependency updates including urllib3 and cryptography. [PR #31](https://github.com/NBChub/bgcflow_wrapper/pull/31), [PR #30](https://github.com/NBChub/bgcflow_wrapper/pull/30)
- **New Contributor**: @dependabot. [PR #31](https://github.com/NBChub/bgcflow_wrapper/pull/31)
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.3.1...v0.3.2)

## 0.3.1 (2023-08-27)
- **Update**: Read project metadata for dbt models synchronization. Manual definition of dbt models to exclude also added.
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.3.0...v0.3.1)

## 0.3.0 (2023-08-26)
- **Docs**: Refer to wiki for tutorial. [PR #26](https://github.com/NBChub/bgcflow_wrapper/pull/26)
- **Feature**: Use metabase API and dbt-metabase for uploading and syncing model relationships. [PR #27](https://github.com/NBChub/bgcflow_wrapper/pull/27)
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.8...v0.3.0)

## 0.2.8 (2023-08-21)
- **Improvement**: Enhanced `mkdocs` report handling, dependency management, and example copying in `bgcflow init`.
- **Update**: Utilize BGCFlow v0.7.2 version dependencies metadata.
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.7...v0.2.8)

## 0.2.7 (2023-08-09)
- **New Feature**: Organize report by subcategory.
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.6...v0.2.7)

## 0.2.6 (2023-08-09)
- **Security Update**: Addressed security concerns.
- **Improvements**: CLI, testing, and new features including panoptes wrapper and subworkflows.
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.5...v0.2.6)

## 0.2.5 (2023-08-01)
- **Fix**: Correct alias parsing to accommodate bgcflow v0.7.0. [PR #20](https://github.com/NBChub/bgcflow_wrapper/pull/20)
- **Chore**: Security update. [PR #21](https://github.com/NBChub/bgcflow_wrapper/pull/21)
- **New Contributor**: @OmkarSaMo. [PR #19](https://github.com/NBChub/bgcflow_wrapper/pull/19)
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.4...v0.2.5)

## 0.2.4 (2023-06-27)
- **Update**: Dependency update for improved stability and performance. [PR #17](https://github.com/NBChub/bgcflow_wrapper/pull/17), [PR #18](https://github.com/NBChub/bgcflow_wrapper/pull/18)
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.3...v0.2.4)

## 0.2.3 (2023-06-15)
- **Fix**: Correct UnicodeEncodeError in Windows. [PR #7](https://github.com/NBChub/bgcflow_wrapper/pull/7)
- **Docs**: Add graphical abstract. [PR #16](https://github.com/NBChub/bgcflow_wrapper/pull/16)
- This release is compatible with BGCFlow version 0.6.1 and version 0.6.2.
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.2-alpha...v0.2.3)

## 0.2.2 (2023-01-30)
- **Pre-release**: Compatibility with BGCFlow 0.6.0.
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.1-alpha...v0.2.2-alpha)

## 0.2.1 (2022-11-18)
- **Migration**: Migrate to [NBChub repo](https://github.com/NBChub/bgcflow_wrapper).
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.2.0...v0.2.1-alpha)

## 0.2.0 (2022-11-18)
- Minor updates and enhancements.
- [Full Changelog](https://github.com/NBChub/bgcflow_wrapper/compare/v0.1.0...v0.2.0)

## 0.1.0 (2022-11-17)
- Initial release of the package.
