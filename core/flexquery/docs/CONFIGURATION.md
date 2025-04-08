
# CONFIGURATION

## COMPONENTS 

### Connection Manager
Handles database connections with details from `profiles.yml` file.

### Query Processor
Executes SQL queries with parameters, returns Pandas DataFrames, .csv or .xlsx files

## DEVELOPER GUIDE 

### Adding a New Environment
1. Add connection details to `profiles.yml`
    - Can be in project root, or
    - The `secrets/` directory one level above your project root
2. Create directory in `queries_library/[ENV_NAME]/`
3. Add `params.yml` in the new environment directory

### Adding a New Query
1. Create `.sql` file in appropriate environment directory
2. Add parameters in format `{{:parameter_name}}`
3. Update environment's `params.yml` if needed

## CONFIG TEMPLATES 

Following configuration files were created for you, please update to your specifications:
1. `profiles.yml`
2. `queries_library\TEST\`
    - `params.yml`
    - `query.sql`

## USAGE EXAMPLES 

Interactive query selection: 
```bash
flexquery run --env DEV
```

Save results to CSV: 
```bash
flexquery run --env PROD --write-csv
```

## HELP 

For more help run: 
```bash
flexquery --help
```
