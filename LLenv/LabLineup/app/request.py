class request:
    def __init__(self, rid, lid, suid, station, description,\
                 timeSubmitted, timeCompleted, huid, feedback):
        self.rid = rid
        self.lid = lid
        self.suid = suid
        self.station = station
        self.description = description
        self.timeSubmitted = timeSubmitted
        self.timeCompleted = timeCompleted
        self.huid = huid
        self.feedback = feedback

    def toString(self):
        finalString = "RID:\t" + self.rid
        finalString = finalString + "\tLID:\t" + self.lid
        finalString = finalString + "\tSUID:\t" + self.suid
        finalString = finalString + "\tStation:\t" + self.station
        finalString = finalString + "\tDescription:\t" + self.description
        finalString = finalString + "\tTime Submitted:\t" + self.timeSubmitted
        finalString = finalString + "\tTime Completed:\t" + self.timeCompleted
        finalString = finalString + "\tHUID:\t" + self.huid
        finalString = finalString + "\tFeedback:\t" + self.feedback
        return finalString

    def timeTaken(self):
        return timeCompleted - timeSubmitted
    
