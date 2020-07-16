package sequences

type SequenceList struct {
	sequenceList []*EventList
}

func (sequenceList *SequenceList) Get() []*EventList {
	return sequenceList.sequenceList
}

func (sequenceList *SequenceList) Append(sequence *EventList) {
	sequenceList.sequenceList = append(sequenceList.sequenceList, sequence)
}

func (sequenceList *SequenceList) Set(sequences []*EventList) {
	sequenceList.sequenceList = sequences
}

func (sequenceList *SequenceList) Len() int{
	return len(sequenceList.sequenceList)
}

func (sequenceList *SequenceList) DropLastItem(){
	sequenceList.sequenceList = sequenceList.sequenceList[:sequenceList.Len() - 1]
}