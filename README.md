# Link to Hugging Face
https://huggingface.co/spaces/Edlevco/BinarySearchProjectCISC121

# search-project
CISC 121 001 - Project 1 - Binary Search Algorithm

Why I chose binary Search:

I chose binary search to research and understand because I find it the most interesting search and most applicable to real life.

Unlike Linear search, binary search uses a more common knowledge approach to finding an index in a sorted array. Linear search finds what it is looking for by checking
every single position. It does this because it has no clues to help it find what it is looking for. This is like finding your friend's locker by opening every locker,
checking if it has your friend's backpack in it. This method is simple and is not effictive. Binary search is interesting to me because it finds the correct index, 
using clues such as higher or lower. With these clues, you can split the total decisions in half until you reach your solution.

In addition to being interesting to me, I use binary search in my day-to-day life. For example, when I am finding a word in the dictionary I use binary search to find the word,
rather than going page by page. Because I know that the dictionary is sorted by letters, I can open up the middle of the book, and I can see whether my word is later in the book,
or closer to the start. 

Step 2 — Plan Using Computational Thinking

· Decomposition: What smaller steps form your algorithm?

The smaller steps that form my algorithm are checking whether the value I'm looking for is greater or less than the value that I am currently checking.
For example, if I check the middle index and it is 40, but I am checking for 30, I would go to a lower index, since the array is already sorted.

· Pattern Recognition: How does it repeatedly compare or swap values?

It repeatedly compares with a while loop. Using two pointers, one at the left side and one at the right. It will find the middle of the two pointers.

If the target number is lower, it will bring down the right pointer to the current index
If the target number is higher, it will bring up the left pointer to the current index

After that, it will find the new middle index and repeat.

· Abstraction: What details are simplified for the user?

The binary search is a sorting algorithm that efficiently finds the target value.

This only works with an indexable, sorted array.


· Algorithm Design: How will input → processing → output flow?

Input: 
The user enters a sorted array and a target number

Processing:
The algorithm will repeatedly search for the target number using the while loop described in pattern recognition,
It does that process until the target number is found or until the left pointer and right pointer are pointing at the same index

Output:
The algorithm will output the index of the target number if it is found, or -1 if the target number is not in the sorted array


