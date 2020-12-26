package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

var usage string = fmt.Sprintf("usage: %s [-h | --help] {one,two}\n", filepath.Base(os.Args[0]))

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

func printUsageAndDie() {
	fmt.Fprintf(os.Stderr, usage)
	os.Exit(1)
}

func printHelp() {
	fmt.Fprintf(os.Stdout, usage)
	fmt.Fprintln(os.Stdout, `Read a list of numbers from stdin and find the combination
	of two or three numbers add up to 2020 and multiply them together.`)
}

func main() {
	if len(os.Args) == 2 {
		if os.Args[1] == "-h" || os.Args[1] == "--help" {
			printHelp()
			os.Exit(0)
		}
		if os.Args[1] != "one" && os.Args[1] != "two" {
			printUsageAndDie()
		}
	} else {
		printUsageAndDie()
	}

	var func2020 func([]int) ([]int, error)
	switch os.Args[1] {
	case "one":
		func2020 = add2020Two
	case "two":
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
