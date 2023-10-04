#pragma once

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <chrono>
#include <iomanip>


class Benchmark
{
public:
    Benchmark(): last_passed_res_(0), start_(std::chrono::steady_clock::now()) {}

    void startTimer()
    {
        start_ = std::chrono::steady_clock::now();
    }

    std::chrono::nanoseconds getPassedTime()
    {
        last_passed_res_ = std::chrono::steady_clock::now() - start_;
        return last_passed_res_;
    }

    std::chrono::nanoseconds getLastPassedRes()
    {
        return last_passed_res_;
    }

private:
    std::chrono::nanoseconds last_passed_res_;
    std::chrono::steady_clock::time_point start_;
};


class ProgressBar
{
public:
    ProgressBar(): cur_depth(depth++) {}

    virtual void update(const std::string& meta = "") = 0;
    virtual double getProgress() = 0;
    virtual void logProgress(const std::string& meta = "") = 0;

protected:

    virtual std::string addIndent() const 
    {
        std::string res;
        for (size_t i = 0; i < cur_depth; ++i)
        {
            res += "   ";
        }
        return res;
    }

    size_t cur_depth;
    static inline size_t depth = 0;
};

class LoopProgress: public ProgressBar
{
public:
    LoopProgress(size_t num_iterations, std::string id, bool only_meta = false): 
        num_iterations_(num_iterations), id_(id), progress_(0), last_log_time_(0), only_meta_(only_meta), ProgressBar() {}

    virtual void update(const std::string& meta = "") override
    {
        ++progress_;
        if (progress_ == num_iterations_)
        {
            logProgress(meta);
            last_log_time_ = bench.getPassedTime();
            --depth;
        }
        else if (std::chrono::duration_cast<std::chrono::seconds>(bench.getPassedTime() - last_log_time_).count() >= 5)
        {
            logProgress(meta);
            last_log_time_ = bench.getLastPassedRes();
        }
    }

    virtual double getProgress() override
    {
        return (double) progress_ / num_iterations_;
    }

    virtual void logProgress(const std::string& meta = "") override
    {
        std::stringstream ss;
        double progress = getProgress();
        size_t passed_time = std::chrono::duration_cast<std::chrono::seconds>(last_log_time_).count();

        if (!only_meta_)
        {
            ss << addIndent() << "== Loop \"" << id_ << "\" | Progress: " << (int)(progress * 100.) << "% | " << 
                passed_time << "s. | Time left: ~" << passed_time * (1 - progress) / progress << " ==";
            std::cout << ss.str();
            if (meta.empty())
            {
                std::cout << '\n';
            }
            else
            {
                std::cout << '\n' << addIndent() << meta << '\n';
            }
        }
        else if (!meta.empty())
        {
            std::cout << addIndent() << meta << '\n';
        }

        if (progress_ == num_iterations_)
        {
            std::cout << addIndent() << std::setw(80) << std::setfill('-') << "| Total time: " << 
                (passed_time == 0 ? "<1" : std::to_string(passed_time))<< "s.\n\n";
        }
        std::cout << '\n';
    }

private:
    bool only_meta_;
    size_t num_iterations_;
    std::string id_;
    size_t progress_;
    std::chrono::nanoseconds last_log_time_;
    Benchmark bench;
};