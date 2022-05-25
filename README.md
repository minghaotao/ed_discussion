# ed_discussion




We are transitioning from Piazza to Ed Discussion this semester. 

I was tasked to pull the data from Ed Discussion courses and calculate the late response rate for overall courses. 

The idea of this project would be automated to send visuals via our Slack channel weekly. 
	
	1. Accessing JSON files and doing the following calculations- 
		a. Covert the timezone to EST (We are based on EST)
		b. Calculate which post has over the 24 hours
			i. Has the answer over 24 hours 
			ii. Didn’t have an answer over the 24 hours
		c. Download calculated course data as CSV file 
			i. Post_url
			ii. Post_create_at
			iii. Answer_at
			iv. Category
			v. Type
			vi. Over_24
	2. Generating report files
		a. Accessing all the local course data files
		b. Do the following calculations
			i. Total_thread (Questions + Posts)
			ii. Total_questions
			iii. Current_unresolved
			iv. Late_24hours (Number)
			v. Response_rate (Late_24hours/Total_questions)
	3. Visualization and send reports to Slack Channel
		a. Use the bar chart via Pandas/matplotlib
		b. Send the charts to the Slack channel
    c. Use Crontab command for scheduled auto-run 

