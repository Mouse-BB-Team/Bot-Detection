branch := $(shell git rev-parse --abbrev-ref HEAD)
jobToExecute =  'example.sh'
periodInMinutes = 1
current_dir := $(PWD)

all: cache_git_credentials make_executive_scripts add_cron_job

cache_git_credentials:
	@echo "Caching git credentials"
	git config credential.helper store

make_executive_scripts:
	@echo "Making executive scripts"
	chmod +x git-observer-cron-job.sh
	chmod +x add-cron-job.sh

add_cron_job:
	@echo "Adding git observer job to cron"
	./add-cron-job.sh $(periodInMinutes) $(current_dir) $(branch) $(jobToExecute)
