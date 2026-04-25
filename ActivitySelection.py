def activity_selection(start, finish):
    # Pair and sort activities by finish time
    activities = sorted(zip(start, finish), key=lambda x: x[1])

    print("\nSorted activities (by finish time):")
    print(f"{'Index':<8} {'Start':<8} {'Finish':<8}")
    print("-" * 24)
    for i, (s, f) in enumerate(activities):
        print(f"{i:<8} {s:<8} {f:<8}")

    # Always select the first activity
    count = 1
    j = 0
    selected = [activities[0]]

    print(f"\nInit → Selected [{activities[0][0]}, {activities[0][1]}]  |  count=1, j=0")

    for i in range(1, len(activities)):
        s, f = activities[i]
        last_s, last_f = activities[j]
        if s > last_f:
            count += 1
            j = i
            selected.append(activities[i])
            print(f"i={i}   → [{s}, {f}]: start {s} > last finish {last_f}  ✓ SELECTED  |  count={count}, j={j}")
        else:
            print(f"i={i}   → [{s}, {f}]: start {s} ≤ last finish {last_f}  ✗ SKIPPED   |  count={count}, j={j}")

    print(f"\nSelected activities: {selected}")
    print(f"Maximum non-overlapping activities: {count}")
    return count


def get_input():
    print("=== Activity Selection Problem (Greedy) ===\n")
    n = int(input("Enter number of activities: "))

    start = []
    finish = []
    print("\nEnter start and finish time for each activity:")
    for i in range(n):
        while True:
            s = int(input(f"  Activity {i} - Start time: "))
            f = int(input(f"  Activity {i} - Finish time: "))
            if f > s:
                start.append(s)
                finish.append(f)
                break
            else:
                print("  Finish time must be greater than start time. Try again.")

    return start, finish


start, finish = get_input()
activity_selection(start, finish)