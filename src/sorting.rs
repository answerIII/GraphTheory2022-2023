use std::{
    ptr::swap,
    sync::{mpsc, Arc, Mutex},
    thread,
};

struct MexicoChecker {
    now: usize,
    len: usize,
}

impl MexicoChecker {
    fn new(len: usize) -> Self {
        MexicoChecker { now: 0, len: len }
    }

    fn add(&mut self, num: usize) {
        self.now += num;
    }

    fn check(&self) -> bool {
        self.len == self.now
    }
}

fn insertion_sort(arr: &mut [i32]) {
    for i in 1..arr.len() {
        let mut j = i as i32 - 1;
        while j >= 0 && arr[j as usize] > arr[j as usize + 1] {
            unsafe { swap(&mut arr[j as usize], &mut arr[j as usize + 1]) }
            j -= 1;
        }
    }
}

fn partition(arr: &mut [i32]) -> usize {
    let mut left = 0;
    let mut right = arr.len() - 1;
    let pivot = arr[(left + right) / 2];
    while left <= right {
        while arr[left] < pivot {
            left += 1;
        }
        while arr[right] > pivot {
            right -= 1;
        }
        if left >= right {
            break;
        }
        unsafe {
            swap(&mut arr[left], &mut arr[right]);
            left += 1;
            right -= 1
        }
    }
    right
}

pub fn quicksort_multi(arr: &mut Vec<i32>, thread_count: usize) {
    let mut threads = Vec::with_capacity(thread_count);
    let mut channels = Vec::with_capacity(thread_count);

    let (tx, rx) = mpsc::channel::<Option<&mut [i32]>>();
    let checker = Arc::new(Mutex::new(MexicoChecker::new(arr.len())));

    for _ in 0..thread_count {
        let cur_tx = tx.clone();
        let (tx, cur_rx) = mpsc::channel::<&mut [i32]>();
        channels.push(tx);
        let checker = Arc::clone(&checker);
        threads.push(thread::spawn(move || {
            for arr in cur_rx {
                if arr.len() <= 25 {
                    insertion_sort(arr);
                    let tmp: bool;
                    {
                        let mut a = checker.lock().unwrap();
                        a.add(arr.len());
                        tmp = a.check();
                    };
                    if tmp {
                        cur_tx.send(None).unwrap();
                    }
                    continue;
                }
                let q = partition(arr);
                let (left, right) = arr.split_at_mut(q + 1);

                cur_tx.send(Some(left)).unwrap();
                cur_tx.send(Some(right)).unwrap();
            }
        }));
    }

    let mut channels_iter = channels.iter().cycle();
    unsafe {
        let s = &mut arr[..];
        let len = s.len();
        let ptr = s.as_mut_ptr();
        let slice = std::slice::from_raw_parts_mut(ptr, len);
        channels_iter.next().unwrap().send(slice).unwrap();
    }

    for i in &rx {
        match i {
            Some(i) => channels_iter.next().unwrap().send(i).unwrap(),
            None => break,
        }
    }

    for i in channels {
        drop(i)
    }

    for i in threads {
        i.join().unwrap();
    }
}
