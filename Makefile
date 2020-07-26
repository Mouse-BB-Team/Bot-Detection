all: make-all-scripts-executable set-connection-with-PLGrid

make-all-scripts-executable:
	chmod +x utils/git-observer/run-commit-execution.sh
	chmod +x utils/git-observer/run-plgrid-job.sh
	chmod +x utils/git-observer/git-push-alias.sh
	chmod +x utils/git-observer/json-parser.sh

set-connection-with-PLGrid:
	@echo "What is your PLGrid username?: "; \
	read USERNAME; \
	ssh-copy-id $$USERNAME@pro.cyfronet.pl; \
	echo "export PLG_USERNAME=$$USERNAME" >> ~/.bashrc; \
	echo "export PLG_USERNAME=$$USERNAME" >> ~/.zshrc; \
	echo "What is the name of branch that you want to observe?: "; \
	read BRANCH; \
	ssh $$USERNAME@pro.cyfronet.pl "echo 'export OBSERVED_BRANCH=$$BRANCH' >> ~/.bashrc && source ~/.bashrc && \
	echo SSH key generation. In all steps press ENTER!!! && \
	ssh-keygen -t rsa -b 2048 && \
	cat ~/.ssh/id_rsa.pub && \
	echo Copy above ssh key to your github account. If you finish, press any key ... && \
	read && \
	git clone git@github.com:Mouse-BB-Team/Bot-Detection.git && \
	chmod +x ./Bot-Detection/utils/git-observer/run-plgrid-job.sh";