import EDSM_generate_reports

# Load the INI file
config = "EDSM_config.ini"

EDSM_generate_reports.EDSM_get_report_system_overview(config)
print('Report 1 ready to report')

EDSM_generate_reports.EDSM_get_report_faction_overview(config)
print('Report 2 ready to report')

EDSM_generate_reports.EDSM_get_report_inf_history(config)
print('Report 3 ready to report')   

EDSM_generate_reports.EDSM_get_system_update_status(config)
print('Report 4 ready to report')