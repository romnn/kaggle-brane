build:
	brane unpublish -f kaggle 1.0.0
	brane remove -f kaggle
	brane build container.yml
	brane push kaggle 1.0.0
