package main

import (
	"testing"
)

func equalSliceInt(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i, n := range a {
		if n != b[i] {
			return false
		}
	}
	return true
}

func TestAdd2020Two(t *testing.T) {
	got, err := add2020Two([]int{1721, 979, 366, 299, 675, 1456})
	if err != nil {
		t.Errorf("Got error: %v", err)
	}
	want := []int{1721, 299}
	if !equalSliceInt(got, want) {
		t.Errorf("Expected %v, got %v", want, got)
	}
}

func TestAdd2020Three(t *testing.T) {
	got, err := add2020Three([]int{1721, 979, 366, 299, 675, 1456})
	if err != nil {
		t.Errorf("Got error: %v", err)
	}
	want := []int{979, 366, 675}
	if !equalSliceInt(got, want) {
		t.Errorf("Expected %v, got %v", want, got)
	}
}
