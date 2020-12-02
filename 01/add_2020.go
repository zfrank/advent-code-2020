package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func add2020Two(numList []int) ([]int, error) {
	for i, num1 := range numList[0 : len(numList)-1] {
		for _, num2 := range numList[i+1:] {
			if num1+num2 == 2020 {
				return []int{num1, num2}, nil
			}
		}
	}
	return []int{-1, -1}, fmt.Errorf("Could not find any matching numbers")
}

func add2020Three(numList []int) ([]int, error) {
	for i, num1 := range numList[0 : len(numList)-2] {
		for j, num2 := range numList[i+1 : len(numList)-1] {
			for _, num3 := range numList[i+j+1:] {
				if num1+num2+num3 == 2020 {
					return []int{num1, num2, num3}, nil
				}
			}
		}
	}
	return []int{-1, -1, -1}, fmt.Errorf("Could not find any matching numbers")
}

func multiplySlice(numList []int) int {
	total := 1
	for _, n := range numList {
		total = total * n
	}
	return total
}

func readStdinOrDie() []int {
	numList := make([]int, 0)
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		num, err := strconv.Atoi(strings.TrimSpace(scanner.Text()))
		if err != nil {
			panic(err)
		}
		numList = append(numList, num)
	}
	if err_scan := scanner.Err(); err_scan != nil {
		panic(err_scan)
	}
	return numList
}

func main() {
	if len(os.Args) != 2 || (os.Args[1] != "2" && os.Args[1] != "3") {
		fmt.Fprintln(os.Stderr, "You must specify one paramter: '2' or '3'.")
		os.Exit(1)
	}
	var func2020 func([]int) ([]int, error)
	switch os.Args[1] {
	case "2":
		func2020 = add2020Two
	case "3":
		func2020 = add2020Three
	}
	numList := readStdinOrDie()
	nums, err := func2020(numList)
	if err != nil {
		panic(err)
	}
	fmt.Println(nums)
	total := multiplySlice(nums)
	fmt.Println(total)
}
