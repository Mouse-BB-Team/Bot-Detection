all: make-all-scripts-executable set-connection-with-PLGrid

make-all-scripts-executable:
	chmod +x utils/prometheus_scripts/run-commit-execution.sh
	chmod +x utils/prometheus_scripts/run-plgrid-job.sh
	chmod +x utils/prometheus_scripts/git-push-alias.sh
	chmod +x utils/prometheus_scripts/create-git-alias.sh

set-connection-with-PLGrid:
	@echo "What is your PLGrid username?: "; \
	read USERNAME; \
	ssh-copy-id $$USERNAME@pro.cyfronet.pl; \
	echo "export PLG_USERNAME=$$USERNAME" >> ~/.bashrc; \
	echo "export PLG_USERNAME=$$USERNAME" >> ~/.zshrc; \
	echo "What is the name of branch that you want to observe?: "; \
	read BRANCH; \
	sh ./utils/prometheus_scripts/create-git-alias.sh; \
	ssh $$USERNAME@pro.cyfronet.pl "echo 'export OBSERVED_BRANCH=$$BRANCH' >> ~/.bashrc && source ~/.bashrc && \
	echo SSH key generation. In all steps press ENTER!!! && \
	ssh-keygen -t rsa -b 2048 && \
	cat ~/.ssh/id_rsa.pub && \
	echo Copy above ssh key to your github account. If you finish, press any key ... && \
	read && \
	git clone git@github.com:Mouse-BB-Team/Bot-Detection.git && \
	chmod +x ~/Bot-Detection/utils/prometheus_scripts/run-plgrid-job.sh && \
	echo 'export NOTIFY=true' >> ~/.bashrc && \
	echo 'export TFHUB_CACHE_DIR=$PLG_GROUPS_STORAGE/plggpchdyplo/cnn_models' >> ~/.bashrc && \
	echo 'export RESULTS_PATH=$PLG_GROUPS_STORAGE/plggpchdyplo/outputs' >> ~/.bashrc";
